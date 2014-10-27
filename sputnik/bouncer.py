#! /usr/bin/env python3 -B

import asyncio
from network import Network
from client import Client

class Bouncer(object):

    def __init__(self):

        self.clients = set()
        self.networks = dict()


    def start(self, hostname="", port=6667):

        loop = asyncio.get_event_loop()
        coroutine = loop.create_server(lambda: Client(self),
                                       hostname, port)
        server = loop.run_until_complete(coroutine)

        try: loop.run_forever()
        except KeyboardInterrupt: pass
        finally: loop.close()

    # @asyncio.coroutine
    def add_network(self, hostname, port):

        loop = asyncio.get_event_loop()
        coro = loop.create_connection(lambda: Network(self,
                                    network="freenode",
                                    nickname="Decepticon1337",
                                    username="Decepticon1337",
                                    realname="Decepticon1337"),
                                    hostname, port)
        loop.run_until_complete(coro)

if __name__ == "__main__":
    bouncer = Bouncer()
    bouncer.add_network("irc.freenode.net", 6667)
    # bouncer.add_network("irc.quakenet.org", 6667)
    # bouncer.add_network("irc.gamesurge.net", 6667)
    bouncer.start()
