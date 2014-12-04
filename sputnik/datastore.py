"""Sputnik Datastore Implementation

This module provides the Sputnik Datastore implementation. It implements a thin
wrapper around Redis, which is required in order to persist data across Bouncer
restarts or network disconnections. This functionality is required due to the
ephemeral filesystems typical to most Platform-as-a-Service Providers (PaaS).
"""

import bcrypt
import json
import os
import redis


class Datastore(object):
    """A singleton that provides a thin wrapper to Redis.

    The Datastore is responsible for persisting networks and channels in the
    event of an unexpected crash by either the Bouncer or a connected network.
    It also holds persistent, shared variables, such as the Bouncer password.

    Attributes:
        database (redis.Redis): A Redis database connection.
    """

    def __init__(self, hostname, port):
        """Creates an instance of a Datastore.

        Connects to a Redis instance running on the given hostname and port.

        Args:
            hostname (str): A hostname for a Redis instance.
            port (int): A port for a Redis instance.
        """

        if hostname and port: redis_url = "redis://%s:%s" % (hostname, port)
        self.database = redis.from_url(os.getenv("REDISTOGO_URL", redis_url))

    def get_networks(self):
        """Retrieves all connected networks from Redis.

        This gets credentials for all connected networks, where credentials
        contain all values necessary to reconstruct a network connection, where
        networks are of the form `{ "<network_name>" : "<credentials>" }`.

        Returns:
            dict: A dictionary of network credentials.
        """

        networks = {}
        for key in self.database.keys("network=*"):
            val = json.loads(self.database.get(key).decode())
            networks[key.decode().split("=")[1]] = val
        return networks

    def get_channels(self, network=""):
        """Retrieves all connected channels from Redis.

        This gets credentials for all connected channels, where credentials are
        of the form `{ "<network/channel>" : "<password>" }`. If the network
        argument is specified, then the output is filtered to only include
        channels from the indicated network.

        Args:
            network (str, optional): The name of a network. Defaults to ``""``.

        Returns:
            dict: A dictionary of channel credentials.
        """

        channels = {}
        for key in self.database.keys("".join(["channel=", network, "*"])):
            password = self.database.get(key).decode() or None
            channels[key.decode().split("=")[1]] = password
        return channels

    def get_password(self):
        """Retrieves the Bouncer password from Redis.

        Returns:
            str: The encrypted Bouncer password.
        """

        password = self.database.get("password=bouncer:password")
        return password.decode() if password else None

    def set_password(self, password="cosmonaut"):
        """Saves a new Bouncer password to Redis.

        Args:
            password (str, optional): The new password for the Bouncer.
        """

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.database.set("password=bouncer:password", hashed_password)

    def check_password(self, password_attempt):
        """Checks a password attempt against the Bouncer password.

        Args:
            password_attempt (str): The password attempt.

        Returns:
            bool: Whether the password matched.
        """

        password = self.get_password()
        return bcrypt.hashpw(password_attempt.encode(), password) == password

    def add_network(self, network, hostname, port,
                    nickname, username, realname,
                    password=None, usermode=0):
        """Adds a network to the Redis instance.

        Args:
            network (str): The name of the IRC network to connect to.
            hostname (str): The hostname of the IRC network to connect to.
            port (int): The port to connect using.
            nickname (str): The IRC nickname to use when connecting.
            username (str): The IRC ident to use when connecting.
            realname (str): The real name of the user.
            password (str, optional): Bouncer password. Defaults to ``None``.
            usermode (int, optional): The IRC usermode. Defaults to ``0``.
        """

        credentials = { "network"  : network,
                        "nickname" : nickname,
                        "username" : username,
                        "realname" : realname,
                        "hostname" : hostname,
                        "port"     : port,
                        "password" : password }

        key = "".join(["network=", network])
        self.database.set(key, json.dumps(credentials))

    def remove_network(self, network):
        """Removes a network from Redis.

        Args:
            network (str): The name of a network to remove.
        """

        key = "".join(["network=", network])
        self.database.delete(key)

    def add_channel(self, network, channel, password=""):
        """Adds a channel to the Redis.

        Args:
            network (str): The name of a network.
            channel (str): The name of a channel.
            password (str, optional): The channel password. Defaults to ``""``.
        """

        key = "".join(["channel=", network, ":", channel])
        self.database.set(key, password or "")

    def remove_channel(self, network, channel):
        """Removes a channel from Redis.

        Args:
            network (str): The name of a network.
            channel (str): The name of a channel.
        """

        key = "".join(["channel=", network, ":", channel])
        self.database.delete(key)
