#! /usr/bin/env python3

import asyncio
from network import Network
from server import Server

class Bouncer(object):

    def __init__(self, hostname="localhost", port=6667):

        loop = asyncio.get_event_loop()
        coroutine = loop.create_server(Server, hostname, port)
        server = loop.run_until_complete(coroutine)

        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try: loop.run_forever()
        except KeyboardInterrupt: pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    Bouncer()
