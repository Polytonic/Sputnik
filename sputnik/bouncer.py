#! /usr/bin/env python3
"""Sputnik Bouncer Implementation

This module provides the Sputnik Bouncer implementation. As the primary entry
point, the Bouncer is responsible for bootstrapping the entire program.
"""

import asyncio
from client import Client
from network import Network
from server import HTTPServer


class Bouncer(object):
    """A singleton that manages connected devices.

    The Bouncer provides the base functionality needed to instantiate a new
    Client or Network. It also acts as a bridge between connected Clients and
    Networks by maintaining an authoritative record of each connected device.

    Attributes:
        clients (set of Client): A set of connected Clients.
        networks (dict of Network): A dictionary of connected Networks.
    """

    def __init__(self):
        """Creates an instance of a Bouncer.

        Initializes an empty set and an empty dictionary for later use.
        """

        self.clients = set()
        self.networks = dict()

    def start(self, hostname="", port=6667):
        """Starts the IRC and HTTP listen servers.

        This creates the IRC server-portion of the Bouncer, allowing it to
        accept connections from IRC clients. It also starts the HTTP server,
        enabling browsers to connect to the web interface.

        Note:
            This is a blocking call.

        Args:
            hostname (str, optional): Hostname to use. Defaults to ``""``.
            port (int, optional): The port to listen on. Defaults to 6667.
        """

        loop = asyncio.get_event_loop()
        coro = loop.create_server(lambda: Client(self),
                                  hostname, port)
        loop.run_until_complete(coro)
        HTTPServer(bouncer).start()

        try: loop.run_forever()
        except KeyboardInterrupt: pass
        finally: loop.close()

    # this is due for a refactor
    # the exact form of this depends on how the web interface is implemented
    def add_network(self, network, hostname, port, nickname,
                    username, realname, password=None):

        loop = asyncio.get_event_loop()
        asyncio.async(loop.create_connection(lambda: Network(self,
                                             network=network,
                                             nickname=nickname,
                                             username=username,
                                             realname=realname,
                                             hostname=hostname,
                                             port=port,
                                             password=password),
                                             hostname, port))

if __name__ == "__main__":
    bouncer = Bouncer()
    bouncer.add_network("freenode", "irc.freenode.net", 6667,
                        "Decepticon1337", "Decepticon1337",
                        "Decepticon1337")
    # bouncer.add_network("quakenet", "irc.quakenet.org", 6667,
    #                     "Decepticon1337", "Decepticon1337",
    #                     "Decepticon1337")
    # bouncer.add_network("gamesurge", "irc.gamesurge.net", 6667,
    #                     "Decepticon1337", "Decepticon1337",
    #                     "Decepticon1337")
    bouncer.start()

    # eventually should implement __init__.py and __main__.py
    # other things ... database logging?
