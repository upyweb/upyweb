import exceptions as errors
import re
from request import HTTPRequest
import hdrs

METHRE = re.compile('[A-Z0-9$-_.]+')
HDRRE = re.compile(b'[\x01-\x1F\x7F()<>@,;:\[\]={} \t\\\\\"]') # pcre can not compile string with 0x00

istr = hdrs.istr

class CIMultiDict(dict):
    def __setitem__(self, key, value):
        key = hdrs.istr(key)
        super(CIMultiDict, self).__setitem__(key, value)

class HttpParser:
    # codes from aiohttp
    def __init__(self, max_line_size=8190, max_headers=32768,
                 max_field_size=8190):
        self.max_line_size = max_line_size
        self.max_headers = max_headers
        self.max_field_size = max_field_size

    def parse_headers(self, lines):
        """Parses RFC 5322 headers from a stream.

        Line continuations are supported. Returns list of header name
        and value pairs. Header name is in upper case.
        """
        close_conn = None
        encoding = None
        headers = CIMultiDict()
        raw_headers = []

        lines_idx = 1
        line = lines[1]

        while line:
            header_length = len(line)

            # Parse initial header name : value pair.
            try:
                bname, bvalue = line.split(b':', 1)
            except ValueError:
                raise errors.InvalidHeader(line) from None

            bname = bname.strip(b' \t').upper()
            if HDRRE.search(bname):
                raise errors.InvalidHeader(bname)

            # next line
            lines_idx += 1
            line = lines[lines_idx]

            # consume continuation lines
            continuation = line and line[0] in (32, 9)  # (' ', '\t')

            if continuation:
                bvalue = [bvalue]
                while continuation:
                    header_length += len(line)
                    if header_length > self.max_field_size:
                        raise errors.LineTooLong(
                            'limit request headers fields size')
                    bvalue.append(line)

                    # next line
                    lines_idx += 1
                    line = lines[lines_idx]
                    continuation = line[0] in (32, 9)  # (' ', '\t')
                bvalue = b'\r\n'.join(bvalue)
            else:
                if header_length > self.max_field_size:
                    raise errors.LineTooLong(
                        'limit request headers fields size')

            bvalue = bvalue.strip()

            name = istr(bname.decode('utf-8', 'surrogateescape'))
            value = bvalue.decode('utf-8', 'surrogateescape')

            # keep-alive and encoding
            if name == hdrs.CONNECTION:
                v = value.lower()
                if v == 'close':
                    close_conn = True
                elif v == 'keep-alive':
                    close_conn = False
            elif name == hdrs.CONTENT_ENCODING:
                enc = value.lower()
                if enc in ('gzip', 'deflate'):
                    encoding = enc

            headers[name] = value
            raw_headers.append((bname, bvalue))

        return (headers, raw_headers, close_conn, encoding)


class HttpRequestParser(HttpParser):
    """Read request status line. Exception errors.BadStatusLine
    could be raised in case of any errors in status line.
    Returns RawRequestMessage.
    """

    def __call__(self, buf):
        # read HTTP message (request line + headers)
        try:
            if type(buf) in [str, bytes]:
                raw_data = buf[:self.max_headers].split(b'\r\n\r\n')[0] + b'\r\n\r\n'
            else:
                raw_data = yield from buf.read(
                    self.max_headers)
                raw_data = raw_data[:self.max_headers].split(b'\r\n\r\n')[0] + b'\r\n\r\n'
        except errors.LineLimitExceededParserError as exc:
            raise errors.LineTooLong(exc.limit) from None

        lines = raw_data.split(b'\r\n')

        # request line
        line = lines[0].decode('utf-8', 'surrogateescape')
        try:
            method, path, version = line.split(None, 2)
        except ValueError:
            raise errors.BadStatusLine(line) from None

        # method
        method = method.upper()
        if not METHRE.match(method):
            raise errors.BadStatusLine(method)

        # version
        try:
            if version.startswith('HTTP/'):
                n1, n2 = version[5:].split('.', 1)
                version = (int(n1), int(n2))
            else:
                raise errors.BadStatusLine(version)
        except:
            raise errors.BadStatusLine(version)

        # read headers
        headers, raw_headers, close, compression = self.parse_headers(lines)
        if close is None:  # then the headers weren't set in the request
            if version <= (1, 0):  # HTTP 1.0 must asks to not close
                close = True
            else:  # HTTP 1.1 must ask to close.
                close = False

        return HTTPRequest(data='',
                           method=method,
                           path=path,
                           version=version,
                           headers=headers,
                           close=close,
                           compression=compression
                           )
