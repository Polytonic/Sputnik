import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, bouncer):
        self.bouncer = bouncer


class MainHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", networks=self.bouncer.networks)


class EditGetHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, network_name):
        network = self.bouncer.networks[network_name]
        self.render("edit.html", network=network)


class EditPostHandler(BaseHandler):
    @tornado.web.addslash
    def post(self):
        network_name = self.get_argument("networkname")
        network_address = self.get_argument("networkaddress")
        nickname = self.get_argument("nickname")
        ident = self.get_argument("ident")

        hostname, port = network_address.split(":")

        network = self.bouncer.networks[network_name]
        network.transport.close()

        self.bouncer.add_network(network=network_name,
                                 hostname=hostname,
                                 port=port,
                                 nickname=nickname,
                                 username=ident,
                                 realname=ident)

        self.redirect("/")


class DeleteHandler(BaseHandler):
    @tornado.web.addslash
    def get(self, network_name):
        if (network_name in self.bouncer.networks):
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

        hostname, port = network_address.split(":")

        if (network_name not in self.bouncer.networks):
            self.bouncer.add_network(network=network_name,
                                     hostname=hostname,
                                     port=port,
                                     nickname=nickname,
                                     username=ident,
                                     realname=ident)

        self.redirect("/")
