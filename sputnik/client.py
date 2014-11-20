"""Sputnik Client Implementation

This module provides the Sputnik Client implementation. This is a subclass of
a Connection, and defines an interface to IRC client applications implementing
_RFC 2812: https://tools.ietf.org/html/rfc2812 .
"""

from connection import Connection


class Client(Connection):
    """An instance of a connection from an IRC client.

    A Client is the product of an asyncio protocol factory, and represents
    an instance of a connection from an IRC client to the listen server. It
    does not implement an actual IRC client, as defined in
    _RFC 2812: https://tools.ietf.org/html/rfc2812 .

    Attributes:
        bouncer (sputnik.Bouncer): A reference to the Bouncer singleton.
        broker (sputnik.Network): The connected Network instance.
        network (str): The name of the IRC network to connect to.
        ready (bool): Indicates if the Client has connected to a Network.
    """

    def __init__(self, bouncer):
        """Creates an instance of a Client.

        The Network and Broker attributes are defined here in order to support
        Look-Before-You-Leap (LBYL). This is an explicit design decision made
        in favor of simplicity and readability. The bouncer reference is needed
        in order to access the list of connected Networks.

        Args:
            bouncer (sputnik.Bouncer): The singleton Bouncer instance.
        """

        self.bouncer = bouncer
        self.network = None
        self.broker = None

    def connection_made(self, transport):
        """Registers the connected Client with the Bouncer.

        Adds the Client to the set of connected Clients in the Bouncer and
        saves the transport for later use.
        """

        print("Client Connected to Bouncer")
        self.bouncer.clients.add(self)
        self.transport = transport
        self.ready = False

    def connection_lost(self, exc):
        """Unregister the connected Client from the Bouncer.

        Removes the Client from the set of connected Clients in the Bouncer
        before the connection is terminated. After this point, there should be
        no remaining references to this instance of the Client.
        """

        print("Client Disconnected from Bouncer")
        self.bouncer.clients.remove(self)

    def data_received(self, data):
        """Handles incoming messages from connected IRC clients.

        Messages coming from IRC clients are potentially batched, and need to
        be parsed into individual lines before any other operation may occur.
        Afterwards, we split lines according to the IRC message format and then
        perform actions as appropriate.
        """

        for line in data.decode().rstrip().split("\r\n"):
            l = line.split(" ", 1)

            if   l[0] == "QUIT": pass  # Suppress the QUIT Command
            elif l[0] == "USER":

                self.network = l[1].split(" ")[0]
                if self.network not in self.bouncer.networks:
                    self.send("This Network Does Not Exist", "[C to D]")
                else: self.broker = self.bouncer.networks[self.network]

            elif l[0] == "JOIN":

                for channel in l[1].split(","):
                    channel = channel.split(" ")
                    password = channel[1] if len(channel) > 1 else None
                    self.bouncer.datastore.add_channel(
                        self.network, channel[0], password)
                self.forward(line)

            elif l[0] == "PART":

                self.bouncer.datastore.remove_channel(
                    self.network, l[1].split(" ")[0])
                self.forward(line)

            else: self.forward(line)

        if self.broker and not self.ready:
            for line in self.broker.server_log: self.send(line)
            self.ready = True

    def forward(self, *args):
        """Writes a message to the Network.

        Because the Client represents an instance of a connection from an IRC
        client, we instead need to write to the transport associated with the
        connected network.

        Args:
            args (list of str): A list of strings to concatenate.
        """

        message = self.normalize(" ".join(args))
        if self.broker:
            self.broker.transport.write(message.encode())
            print("[C to B]\t%s" % message, end="")
