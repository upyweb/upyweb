import uasyncio as asyncio
import parsers
import response
import re


async def index(request):
	resp = response.HttpResponse(b"You daye")

	return resp

URL_PATTERNS = (
	("/index/(?P<name>\w+)", index)
)

RE_NAMES = re.compile(r'\?P(\w+)')
def named_findall(regex, s):
	names = RE_NAMES.findall(regex)
	values = re.findall(regex, s)
	if len(values) > 1:
		values = values[0]

	return dict(zip(names, values))

async def serve(reader, writer):
	parser = parsers.HttpRequestParser()
	request = await parser(reader)
	print(request)

	resp = response.HTTPResponse(body=b"Hi guy")

	await writer.awrite(resp.http_body)
	await writer.aclose()
	#return response.HttpResponse()

import logging
#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
#mem_info()
loop.call_soon(asyncio.start_server(serve, "127.0.0.1", 8081))
loop.run_forever()
loop.close()
