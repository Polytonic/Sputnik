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

                self.username, self.network = l[1].split(" ")[0].split("/")
                if self.network not in self.bouncer.networks:
                    self.send("This Network Does Not Exist", "[C to D]")
                else: self.broker = self.bouncer.networks[self.network]

            else: self.forward(line)

        # this prints the server connection log
        # there is a race condition here

        if self.broker and not self.ready:
            [self.send(line) for line in self.broker.server_log]
            self.ready = True

        # can try to message the client, say "I'm not ready yet, and then
        # terminate the connection?"
        # need to check IRC status code and bundle this into the "USER" check

    # this will eventually be refactored into the Connection class
    # ideally accepting the Transport directly, with control flow logic moved
    # back into the controller (i.e. data_received)
    def forward(self, *args):

        message = self.normalize(" ".join(args))
        if self.broker:
            self.broker.transport.write(message.encode())
            print("[C to B]\t%s" % message, end="")
