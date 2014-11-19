"""Sputnik Datastore Implementation

This module provides the Sputnik Datastore implementation. It defines the 
behaviors necessary to store and reload channels and networks should the bouncer ever
unexpectedly go offline. It also stores the bouncer's password in the database.
"""

import redis
import json
import bcrypt

class Datastore(object):
    """A singleton that stores all channels and networks connected to by the bouncer.

    The Datastore is a feature that stores channel and network information in a database
    so that the bouncer can automatically reconnect to channels and networks in the event
    that the bouncer unexpectedly goes offline and must be restarted. It also stores the
    bouncer's password in the database.

    Attributes:
        database (redis database): A redis database session.
    """

    def __init__(self, hostname="localhost", port=6379):
        """Creates an instance of a Datastore.

        Initializes a connection to the database.

        Args:
            hostname (str): The hostname for the redis database.
            port (int): The port for the redis database.
        """

        self.database = redis.StrictRedis(host=hostname, port=port, db=0)

    def get_networks(self):
        """Gets dictionary of network information from database.

        Returns:
            dict = A dictionary of IRC network information.::

                {
                    'network=<network>' :
                        {
                            'hostname':'<hostname>',
                            'port':<port>,
                            'nickname':'<nickname>',
                            'username':'<username>',
                            'realname':'<realname>',
                            'password':'<password>',
                            'usermode':<usermode>
                        }
                }
        """

        networks = {}
        for key in self.database.keys("network=*"):
            json_val = self.database.get(key).decode()
            val = json.loads(json_val)
            networks[key.decode().split("=")[1]] = val
        return networks


    def get_channels(self):
        """Gets dictionary of channel information from database.

        Returns:
            dict = A dictionary of channel information.::

                { 'channel=<network>/<channel>' : '<password>' }
        """

        channels = {}
        for key in self.database.keys("channel=*"):
            password = self.database.get(key).decode() or None
            channels[key.decode().split("=")[1]] = password
        return channels

    def set_password(self, password="cosmonaut"):
        """Saves a new bouncer password to the database.

        Args:
            password (str): The new password for the database.
        """

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.database.set("password=bouncer:password", hashed_password)

    def get_password(self):
        """Fetches and returns the bouncer password from the database.

        Return:
            bytes: The encrypted bouncer password.  Check using bcrypt library.
        """

        return self.database.get("password=bouncer:password")

    def add_network(self, network, hostname, port, nickname, username, realname,
                    password=None, usermode=0):
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

        val =   {
                    "hostname":hostname,
                    "port":port,
                    "nickname":nickname,
                    "username":username,
                    "realname":realname,
                    "password":password,
                    "usermode":usermode
                }
        json_val = json.dumps(val)
        key = ''.join(("network=", network))
        self.database.set(key, json_val)

    def remove_network(self, network):
        """Removes a network from the networks dictionary and underlying database.

        Args:
            network (str): The identifying string for an IRC network.
        """

        key = ''.join(("network=", network))
        self.database.delete(key)

    def add_channel(self, network, channel, password=""):
        """Adds a channel to the channels dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            channel (str): The name of a channel on the IRC network.
            password (str, optional): The password for connection to the channel.
        """

        key = ''.join(("channel=", network, ":", channel))
        #ensure that None passwords are converted to empty strings for storage
        self.database.set(key, password or "")

    def remove_channel(self, network, channel):
        """Removes a channel from the channel dictionary and underlying database.

        Args:
            network (str): The address for an IRC network.
            channel (str): The name of a channel on the IRC network.
        """

        key = ''.join(("channel=", network, ":", channel))
        self.database.delete(key)
