import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, bouncer):
        self.bouncer = bouncer

    def get(self):
        servers_list = [dict(name='Freenode',
                             address='irc.freenode.net',
                             nickname='test nickname',
                             ident='test ident'),
                        dict(name='test_server 2')]

        self.render("index.html", servers_list=servers_list)


class EditHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("example_missing_template.html")
