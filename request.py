class HTTPRequest:
    def __init__(self,
                 data,
                 method,
                 path,
                 version,
                 headers,
                 close,
                 compression):
        self.data = data
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.close = close
        self.compression = compression

    def __repr__(self):
        return '<HTTPRequest %s %s>' % (self.method, self.path)