import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class EditHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("example_missing_template.html")
