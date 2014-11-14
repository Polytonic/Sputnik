import websettings
from tornado import gen
from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web
import tornado.httpserver
from tornado.ioloop import IOLoop
import os


class WebServer(object):
    def __init__(self):
        AsyncIOMainLoop().install()

    def start(self, port):
        application = Application()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(port)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/edit", EditHandler)
        ]
        settings = {
            "template_path": websettings.TEMPLATE_PATH,
            "static_path": websettings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(websettings.WEB_ROOT, "index.html"))


class EditHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(websettings.WEB_ROOT, "edit_server.html"))

