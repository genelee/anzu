#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 W-Mark Kubacki; wmark@hurrikane.de
#

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.locale

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # you don't need following line in templates
        _ = self.locale.translate
        self.write(_("Current locale is %s from the available %s.")
            % (self.locale.code, tornado.locale.get_supported_locales()))

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    tornado.locale.load_translations(os.path.join(cwd, "locales"), "messages")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
