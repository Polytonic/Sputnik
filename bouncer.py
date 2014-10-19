#! /usr/bin/env python3

import asyncio
from network import Network
from server import Server

class Bouncer(object):

    def start(self, hostname="", port=443):

        loop = asyncio.get_event_loop()
        coroutine = loop.create_server(Server, hostname, port)
        server = loop.run_until_complete(coroutine)
        print("Starting Server")
        try: loop.run_forever()
        except KeyboardInterrupt: pass
        finally: loop.close()

    # @asyncio.coroutine
    def add_network(self, hostname, port):

        loop = asyncio.get_event_loop()
        coro = loop.create_connection(Network, hostname, port)
        loop.run_until_complete(coro)

if __name__ == "__main__":
    bouncer = Bouncer()
    # bouncer.add_network("irc.freenode.net", 6667)
    # bouncer.add_network("irc.quakenet.org", 6667)
    # bouncer.add_network("irc.efnet.org", 6667)
    bouncer.start()
