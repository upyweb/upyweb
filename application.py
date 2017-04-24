import uasyncio as asyncio


class Application:
    def __init__(self):
        pass

    def _request_handler(self, reader, writer):
        self._reader = reader
        self._writer = writer

    def run(self, host="127.0.0.1", port=8000, debug=False):
        loop = asyncio.get_event_loop()

        self._debug = debug
        if self._debug:
            print("* Running on http://{host}:{port}" % locals())

        loop.create_task(asyncio.start_server(self._request_handler, host, port))
        loop.run_forever()

        if self._debug:
            print('* Server terminated.')
        loop.close()