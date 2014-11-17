import tornado.web

class NetworkEntry(tornado.web.UIModule):
    def render(self, network, network_controls=False, disabled=False):
        return self.render_string("network-entry.html",
                                  network=network,
                                  network_controls=network_controls,
                                  disabled=disabled)
