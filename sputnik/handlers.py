import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, bouncer):
        self.bouncer = bouncer


class MainHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", networks=self.bouncer.networks)


class EditHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, network_name):
        network = self.bouncer.networks[network_name]
        self.render("edit.html", network=network)

    @tornado.web.addslash
    def post(self, network_name):
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
    @tornado.web.addslash
    def get(self, network_name):
        if network_name in self.bouncer.networks:
            network = self.bouncer.networks[network_name]
            network.transport.close()

        self.redirect("/")


class AddHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render("add.html")

    @tornado.web.addslash
    def post(self):
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
