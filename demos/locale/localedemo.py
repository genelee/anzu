#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 W-Mark Kubacki; wmark@hurrikane.de
#

import os.path
import anzu.httpserver
import anzu.ioloop
import anzu.web
import anzu.locale

class MainHandler(anzu.web.RequestHandler):
    def get(self):
        # you don't need following line in templates
        _ = self.locale.translate
        self.write(_("Current locale is %s from the available %s.")
            % (self.locale.code, anzu.locale.get_supported_locales(MainHandler)))

application = anzu.web.Application(trivial_handlers={
    "/": MainHandler,
})

if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    anzu.locale.load_gettext_translations(os.path.join(cwd, "locales"), "messages")
    http_server = anzu.httpserver.HTTPServer(application)
    http_server.listen(8888)
    anzu.ioloop.IOLoop.instance().start()
