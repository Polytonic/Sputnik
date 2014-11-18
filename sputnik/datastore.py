"""Sputnik DataStore Implementation

This module provides the Sputnik DataStore implementation. It defines the 
behaviors necessary to store and reload channels and networks should the bouncer ever
unexpectedly go offline.
"""

import redis
import json

class DataStore(object):
    """A singleton that stores all channels and networks connected to by the bouncer.

    The DataStore is a feature that stores channel and network information in a database
    so that the bouncer can automatically reconnect to channels and networks in the event
    that the bouncer unexpectedly goes offline and must be restarted.  The primary function
    of this class is to act as a write-through cache for channel and network information
    and act as a wrapper around a redis database that stores this information.

    Attributes:
        channels (dict of str): A dictionary of stored channel information.
            key = '<network>:<channel>'
            value = '<password>'
        networks (dict of dict): A dictionary of stored network information.
            key = '<network>'
            value = {hostname':'<hostname>', 'port':<port>, 'nickname':'<nickname>',
                    'username':'<username>', 'realname':'<realname>', 'password':'<password>',
                    'usermode':<usermode>}
        _database (redis database): A redis database session.
    """
    def __init__(self):
        """Creates an instance of a DataStore.

        Initializes an empty dictionary of channel info and populates it with
        entries stored in the database.
        """

        self.channels = {}
        self.networks = {}
        self._database = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._load_from_database()

    def _load_from_database(self):
        """Loads info stored in the database into the DataStore's dictionaries.
        """

        for key in self._database.keys("*"):
            decoded_key = key.decode()

            #If this is a channel
            if ":" in decoded_key:
                password = self._database.get(key).decode()
                if password == "":
                    password = None
                self.channels[decoded_key] = password

            #If this is a network
            else:
                json_val = self._database.get(key).decode()
                val = json.loads(json_val)
                self.networks[decoded_key] = val

    def add_network(self, network, hostname, port, nickname, username, realname, password = None, usermode = 0):
        """Adds a network to the networks dictionary and underlying database.

        Args:
            network (str): The identifying string for the IRC network.
            hostname (str): The hostname for connecting to the IRC network.
            port (int): The port for connecting to the IRC network.
            nickname (str): The nickname for an account on the IRC network.
            username (str): The username for an account on the IRC network.
            realname (str): The realname for an account on the IRC network.
            password (str): The password for an account on the IRC network.
            usermode (int): The usermode for connecting to the IRC network.
        """

        val = {"hostname":hostname, "port":port, "nickname":nickname,
                "username":username, "realname":realname, "password":password,
                "usermode":usermode}
        self.networks[network] = val
        json_val = json.dumps(val)
        self._database.set(network, json_val)

    def remove_network(self, network):
        """Removes a network from the networks dictionary and underlying database.

        Args:
            network (str): The identifying string for an IRC network.
        """

        self.networks.pop(network, None)
        self._database.delete(network)

    def add_channel(self, network, channel, password = None):
        """Adds a channel to the channels dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            channel (str): The name of a channel on the IRC network.
            password (str, optional): The password for connection to the channel.
        """

        key = ":".join([network, channel])
        self.channels[key] = password
        if password is None:
            password = ""
        self._database.set(key, password)

    def remove_channel(self, network, channel):
        """Removes a channel from the channel dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            channel (str): The name of a channel on the IRC network.
        """

        key = ":".join([network, channel])
        self.channels.pop(key, None)
        self._database.delete(key)
