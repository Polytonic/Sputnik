"""Sputnik ChanSaver Implementation

This module provides the Sputnik ChanSaver implementation. It defines the 
behaviors necessary to store and reload channels should the bouncer ever
unexpectedly go offline.
"""

import redis
import pickle

class Channel(object):
    """A struct of channel information for an IRC network.

    A Channel is a struct of information necessary to identify and connect to a
    channel on any given IRC network.  It is used by the ChanSaver to retain
    channel information if the bouncer were to go down for the purposes of
    automatic channel reconnections.

    Attributes:
        network (str): The network address for the IRC network that the channel is on.
        name (str): The name of the Channel on the IRC network.
        password (str): The password necessary to connect to the Channel.
    """
    def __init__(self, network, name, password = ""):
        """Creates an instance of a Channel using the given arguments.

        Args:
            network (str): The network address for the IRC network that the channel is on.
            name (str): The name of the channel.
            password (str, optional): The password for the channel.
        """

        self.network = network
        self.name = name
        self.password = password

    def __repr__(self):
        """Formatted output for Channel objects.
        """

        return "<Channel(network='%s', name='%s', password='%s')>" % (self.network, self.name, self.password)

class ChanSaver(object):
    """A singleton that stores all channels connected to by the bouncer.

    The ChanSaver is a feature that stores channel information in a database
    so that the bouncer can automatically reconnect to channels in the event
    that the bouncer unexpectedly goes offline and must be restarted.

    Attributes:
        channels (dict of Channel): A dictionary of stored Channel objects.
        _database (redis database): A redis database session.
    """
    def __init__(self):
        """Creates an instance of a ChanSaver.

        Initializes an empty dictionary of Channel objects and populates it with
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
            chan = pickle.loads(self._database.get(key))
            self.channels[self._generate_key(chan.network, chan.name)] = chan

    def _generate_key(self, network, name):
        """Generates a key from an IRC network and a channel name.

        Used internally for dictionary and database management.

        Args:
            network (str): The address for an IRC network.
            name (str): The name of a channel on the IRC network.

        Return:
            (str):  Internal key for given IRC network and channel name.
        """

        return network + ":" + name

    def add_channel(self, network, name, password = ""):
        """Adds a channel to the channels dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            name (str): The name of a channel on the IRC network.
            password (str, optional): The password for connection to the channel.
        """

        chan = Channel(network, name, password)
        key = self._generate_key(network, name)
        self.channels[key] = chan
        self._database.set(key, pickle.dumps(chan))

    def remove_channel(self, network, name):
        """Removes a channel from the channel dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            name (str): The name of a channel on the IRC network.
        """

        key = self._generate_key(network, name)
        self.channels.pop(key, None)
        self._database.delete(key)