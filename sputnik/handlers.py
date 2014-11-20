"""Sputnik Tornado Web RequestHandlers Implementation

This module provides the Sputnik Tornado Web RequestHandlers implementation.
RequestHandlers handle GET and POST requests sent from the web interface.
"""

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """The base RequestHandler that stores the bouncer for RequestHandlers."""

    def initialize(self, bouncer):
        """Initializes this RequestHandler and stores the bouncer.

        Args:
            bouncer (sputnik.Bouncer): The singleton Bouncer instance.
        """

        self.bouncer = bouncer


class MainHandler(BaseHandler):
    """The main RequestHandler that serves the home page.

    The home page displays the current list of networks.
    """

    @tornado.web.addslash
    def get(self):
        """Renders the home page.

        The home page displays the current list of networks.
        """

        self.render("index.html", networks=self.bouncer.networks)


class EditHandler(BaseHandler):
    """The RequestHandler that serves the edit network page.

    The edit network page uses a form to receive updated settings from users.
    When a network is editted, it is disconnected and then recreated using the
    new settings.
    """

    @tornado.web.addslash
    def get(self, network_name):
        """Renders the edit network page.

        The edit network page shows current settings for a network and provides
        a form for submitting changes to that network.

        Args:
            network_name (str): Network name of the network to edit.
        """

        network = self.bouncer.networks[network_name]
        self.render("edit.html", network=network)

    @tornado.web.addslash
    def post(self, network_name):
        """Handles edit network requests.

        The existing network is disconnected and a new connection is started
        using the new settings.

        Args:
            network_name (str): Network name of the network to edit.
        """

        network = self.bouncer.networks[network_name]
        network.transport.close()

        network_name = self.get_argument("networkname")
        network_address = self.get_argument("networkaddress")
        nickname = self.get_argument("nickname")
        ident = self.get_argument("ident")
        password = self.get_argument("password")

        hostname, port = network_address.split(":")

        self.bouncer.add_network(network=network_name,
                                 hostname=hostname,
                                 port=port,
                                 nickname=nickname,
                                 username=ident,
                                 realname=ident,
                                 password=password)

        self.redirect("/")


class DeleteHandler(BaseHandler):
    """The RequestHandler that handles delete network requests."""

    @tornado.web.addslash
    def get(self, network_name):
        """Handles delete network requests.

        Args:
            network_name (str): Network name of the network to delete.
        """

        if network_name in self.bouncer.networks:
            network = self.bouncer.networks[network_name]
            network.transport.close()

        self.redirect("/")


class AddHandler(BaseHandler):
    """The RequestHandler that serves the add network page.

    The add network page uses a form to receive new network settings.
    If a network already exists using the provided name, the network
    is not added.
    """

    @tornado.web.addslash
    def get(self):
        """Renders the add network page.

        The add network page provides a form for adding a new network,
        complete with placeholder settings.
        """

        self.render("add.html")

    @tornado.web.addslash
    def post(self):
        """Handles add network requests.

        If a network already exists using the provided name, the network is
        not added.
        """

        network_name = self.get_argument("networkname")
        network_address = self.get_argument("networkaddress")
        nickname = self.get_argument("nickname")
        ident = self.get_argument("ident")
        password = self.get_argument("password")

        hostname, port = network_address.split(":")

        if network_name not in self.bouncer.networks:
            self.bouncer.add_network(network=network_name,
                                     hostname=hostname,
                                     port=port,
                                     nickname=nickname,
                                     username=ident,
                                     realname=ident,
                                     password=password)

        self.redirect("/")
