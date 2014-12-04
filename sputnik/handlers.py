"""Sputnik Request Handlers

This module provides Tornado Request Handlers for the Sputnik Web Interface.
"""

import tornado.web
import os


class BaseHandler(tornado.web.RequestHandler):
    """A base handler that stores the Bouncer singleton."""

    def initialize(self, bouncer):
        """Initializes the RequestHandler and stores the Bouncer.

        Args:
            bouncer (sputnik.Bouncer): The singleton Bouncer instance.
        """

        self.bouncer = bouncer

        self.env = {}

        self.env["connect_string"] = ":".join(filter(None,
            [os.getenv("RUPPELLS_SOCKETS_FRONTEND_URI"),
             os.getenv("RUPPELLS_SOCKETS_LOCAL_PORT")]))

    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    """The main RequestHandler that serves the home page.

    The home page displays the current list of networks.
    """

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self):
        """Renders the home page.

        The home page displays the current list of networks.
        """

        self.render("index.html", networks=self.bouncer.networks,  **self.env)


class EditHandler(BaseHandler):
    """The RequestHandler that serves the edit network page.

    The edit network page uses a form to receive updated settings from users.
    When a network is editted, it is disconnected and then recreated using the
    new settings.
    """

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self, network_name):
        """Renders the edit network page.

        The edit network page shows current settings for a network and provides
        a form for submitting changes to that network.

        Args:
            network_name (str): Network name of the network to edit.
        """

        network = self.bouncer.networks[network_name]
        self.render("edit.html", network=network,  **self.env)

    @tornado.web.authenticated
    @tornado.web.addslash
    def post(self, network_name):
        """Handles edit network requests.

        The existing network is disconnected and a new connection is started
        using the new settings.

        Args:
            network_name (str): Network name of the network to edit.
        """

        self.bouncer.remove_network(network_name)

        network_name = self.get_argument("networkname")
        network_address = self.get_argument("networkaddress")
        nickname = self.get_argument("nickname")
        realname = self.get_argument("realname")
        ident = self.get_argument("ident")
        password = self.get_argument("password")
        hostname, port = network_address.split(":")

        self.bouncer.add_network(network=network_name,
                                 hostname=hostname,
                                 port=port,
                                 nickname=nickname,
                                 realname=realname,
                                 username=ident,
                                 password=password)

        self.redirect("/")


class DeleteHandler(BaseHandler):
    """The RequestHandler that handles delete network requests."""

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self, network_name):
        """Handles delete network requests.

        Args:
            network_name (str): Network name of the network to delete.
        """

        self.bouncer.remove_network(network_name)
        self.redirect("/")


class AddHandler(BaseHandler):
    """The RequestHandler that serves the add network page.

    The add network page uses a form to receive new network settings.
    If a network already exists using the provided name, the network
    is not added.
    """

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self):
        """Renders the add network page.

        The add network page provides a form for adding a new network,
        complete with placeholder settings.
        """

        self.render("add.html",  **self.env)

    @tornado.web.authenticated
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


class LoginHandler(BaseHandler):
    """The RequestHandler that serves the login page.

    The login page prompts the user for their password and authenticates them
    when the password matches the one stored by the bouncer in its database.
    """

    @tornado.web.addslash
    def get(self):
        """Renders the login page.

        The login page uses a form to ask the user for their password.
        """

        self.render("login.html",  **self.env)

    @tornado.web.addslash
    def post(self):
        """Handles login requests.

        Checks the password against the stored password and authenticates.
        """

        password = self.get_argument("password")

        if self.bouncer.datastore.check_password(password):
            self.set_secure_cookie("user", "securestringneeded")

        self.redirect("/")


class LogoutHandler(BaseHandler):
    """The RequestHandler that handles log out requests.

    Redirects to the homepage after clearing authentication.
    """

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self):
        """Handles log out requests.

        Redirects to the homepage after clearing authentication.
        """

        self.clear_cookie("user")
        self.redirect("/")


class SettingsHandler(BaseHandler):
    """The RequestHandler that serves the settings page.

    Allows users to change their password.
    """

    @tornado.web.authenticated
    @tornado.web.addslash
    def get(self):
        """Renders the settings page.

        The settings page uses a form to allow users to change their password.
        """

        self.render("settings.html",  **self.env)

    @tornado.web.authenticated
    @tornado.web.addslash
    def post(self):
        """Handles settings requests.

        Change password requests require the current password to match and
        two entries of the new password to match.
        """

        current = self.get_argument("current-password")
        new_1 = self.get_argument("new-password-1")
        new_2 = self.get_argument("new-password-2")

        if self.bouncer.datastore.check_password(current) and new_1 == new_2:
            self.bouncer.datastore.set_password(new_1)

        self.render("settings.html",  **self.env)
