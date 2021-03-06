"""Sputnik Network Implementation

This module provides the Sputnik Network implementation. This is a subclass of
a Connection, and defines an interface to IRC server networks implementing
_RFC 2813: https://tools.ietf.org/html/rfc2813 .
"""

from collections import deque
from connection import Connection


class Network(Connection):
    """An instance of a connection to an IRC network.

    A Network is the product of an asyncio protocol factory, and represents an
    instance of a connection from an IRC client to an IRC server. This could
    be either a single IRC server, or more likely, a network of servers behind
    a load balancer. It does not implement an actual IRC server, as defined in

    Attributes:
        ??? (revisit this later)
    """

    def __init__(self, bouncer, network, hostname, port,
                 nickname, username, realname,
                 password=None, usermode=0):
        """Creates an instance of a Network.

        This performs a minimum level of string formatting and type coercion in
        order to conform to the IRC specifications during the connection stage.

        Args:
            bouncer (sputnik.Bouncer): The singleton Bouncer instance.
            network (str): The name of the IRC network to connect to.
            hostname (str): The hostname of the IRC network to connect to.
            port (int): The port to connect using.
            nickname (str): The IRC nickname to use when connecting.
            username (str): The IRC ident to use when connecting.
            realname (str): The real name of the user.
            password (str, optional): Bouncer password. Defaults to ``None``.
            usermode (int, optional): The IRC usermode. Defaults to ``0``.
        """

        self.usermode = str(usermode)
        self.username = username
        self.nickname = nickname
        self.password = password
        self.realname = realname
        self.bouncer = bouncer
        self.network = network
        self.hostname = hostname
        self.port = port

    def connection_made(self, transport):
        """Registers the connected Network with the Bouncer.

        Adds the Network to the set of connected Networks in the Bouncer and
        saves the transport for later use. This also creates a collection of
        buffers and logging facilities, and initiates the authentication
        handshake, if applicable.
        """

        print("Bouncer Connected to Network")
        if self.network in self.bouncer.networks:
            self.bouncer.networks[self.network].transport.close()
        self.bouncer.networks[self.network] = self

        self.connected = True
        self.transport = transport
        self.linebuffer = ""
        self.server_log = []
        self.chat_history = deque()

        self.send("PASS", self.password) if self.password else None
        self.send("NICK", self.nickname)
        self.send("USER", self.username, self.usermode, "*",
                  ":%s" % self.realname)

        if self.bouncer.datastore:
            channels = self.bouncer.datastore.get_channels(self.network)
            for channel_info, password in channels.items():
                channel_name = channel_info.split(":")[1]
                self.send("JOIN", channel_name, password or "")

    def attempt_reconnect(self, attempt=0, retries=5):
        """Attempts to reconnect to a network that unexpectedly disconnected.

        This is only called if we drop the connection to a network and the
        connected flag is set, to distinguish from intentional disconnects.

        Args:
            attempt (int): The current attempt count.
            retries (int): The number of times to attempt to reconnect.
        """

        if attempt <= retries:

            network = self.bouncer.add_network(
                self.network, self.hostname, self.port,
                self.nickname, self.username,
                self.password, self.usermode)

            if network.connected: return
            asyncio.sleep(2**attempt)
            self.attempt_reconnect(attempt + 1)

    def connection_lost(self, exc):
        """Unregisters the connected Network from the Bouncer.

        Removes the Network from the dictionary of connected Clients in the
        Bouncer before the connection is terminated. After this point, there
        should be no remaining references to this instance of the Network.
        """
        self.bouncer.networks.pop(self.network)
        if not self.connected:
            print("Bouncer Disconnected from Network")
        else: self.attempt_reconnect()

    def data_received(self, data):
        """Handles incoming messages from connected IRC networks.

        Messages coming from IRC networks are potentially batched and need to
        be parsed into individual lines before any other operation may occur.
        On certain occasions, incoming data may overflow the transport buffer,
        requiring additional logic to reconstitute the messages into a single
        stream. Afterwards, we split lines according to the IRC message format
        and perform actions as appropriate.
        """

        data = self.decode(data)
        if not data.endswith("\r\n"):
            self.linebuffer += data
            return

        for line in (self.linebuffer + data).rstrip().split("\r\n"):

            print("[N to B]\t%s" % line)

            l = line.split(" ", 2)
            if   l[0] == "PING": self.send("PONG", l[1])
            elif l[1] == "PONG": self.forward("PONG", l[2])
            elif l[0] == "PRIVMSG" or l[1] == "PRIVMSG":

                self.chat_history.append(line)

            else:

                self.chat_history.append(line)
                self.server_log.append(line)

        self.linebuffer = ""

        if self.bouncer.clients:
            while self.chat_history:
                line = self.chat_history.popleft()
                self.forward(line)

    def forward(self, *args):
        """Writes a message to all connected CLients.

        Because the Network represents an instance of a connection to an IRC
        network, we instead need to write to the transports of all clients.

        Args:
            args (list of str): A list of strings to concatenate.
        """

        message = self.normalize(" ".join(args))
        for client in self.bouncer.clients:
            if client.broker == self:
                client.transport.write(message.encode())
                print("[B to C]\t%s" % message, end="")
