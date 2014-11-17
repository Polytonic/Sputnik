import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, bouncer):
        self.bouncer = bouncer


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html", networks=self.bouncer.networks)


class EditHandler(BaseHandler):
    def get(self):
        network_name = self.request.path.split('/')[2]
        network = self.bouncer.networks[network_name]
        self.render("edit.html", network=network)


class AddHandler(BaseHandler):
    def get(self):
        self.render("add.html")
