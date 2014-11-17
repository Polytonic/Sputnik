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


class AddHandler(BaseHandler):
    @tornado.web.addslash
    def get(self):
        self.render("add.html")
