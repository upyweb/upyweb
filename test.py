a = b'GET / HTTP/1.1\r\n\r\nasdada'
import parsers
q = parsers.HttpRequestParser()
w = q(a)
t = w.send(None)
