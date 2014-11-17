"""Sputnik ChanSaver Implementation

This module provides the Sputnik ChanSaver implementation. It defines the 
behaviors necessary to store and reload channels should the bouncer ever
unexpectedly go offline.
"""

import redis

class ChanSaver(object):
    """A singleton that stores all channels connected to by the bouncer.

    The ChanSaver is a feature that stores channel information in a database
    so that the bouncer can automatically reconnect to channels in the event
    that the bouncer unexpectedly goes offline and must be restarted.

    Attributes:
        channels (dict of str): A dictionary of stored channel information.
            key = '<network>:<channel>'
            value = <password>
        _database (redis database): A redis database session.
    """
    def __init__(self):
        """Creates an instance of a ChanSaver.

        Initializes an empty dictionary of channel info and populates it with
        entries stored in the database.
        """

        self.channels = {}
        self._database = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._load_channels_from_database()

    def _load_channels_from_database(self):
        """Loads channels stored in the database into the ChanSaver's channels
        dictionary.
        """

        keys = self._database.keys("*")
        for key in keys:
            password = self._database.get(key).decode("utf-8")
            if password == "":
                password = None
            self.channels[key.decode("utf-8")] = password

    def add_channel(self, network, name, password = None):
        """Adds a channel to the channels dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            name (str): The name of a channel on the IRC network.
            password (str, optional): The password for connection to the channel.
        """

        key = ":".join([network, name])
        self.channels[key] = password
        if password is None:
            password = ""
        self._database.set(key, password)

    def remove_channel(self, network, name):
        """Removes a channel from the channel dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            name (str): The name of a channel on the IRC network.
        """

        key = ":".join([network, name])
        self.channels.pop(key, None)
        self._database.delete(key)