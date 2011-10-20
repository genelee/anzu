#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2011 W-Mark Kubacki; wmark@hurrikane.de
#

import anzu.httpserver
import anzu.ioloop
import anzu.options
import anzu.web

import os.path
import anzu.locale

from anzu.options import define, options, enable_pretty_logging

define("port", default=8888, help="run on the given port", type=int)


@anzu.web.location('/')
class MainHandler(anzu.web.RequestHandler):
    def get(self):
        # you don't need following line in templates
        _ = self.locale.translate
        self.write(_("Current locale is %s from the available %s.")
            % (self.locale.code, anzu.locale.get_supported_locales(MainHandler)))


def main():
    enable_pretty_logging()

    # These two lines are the difference. By them translations are loaded.
    cwd = os.path.dirname(__file__)
    anzu.locale.load_gettext_translations(os.path.join(cwd, "locales"), "messages")

    # here is nothing special
    anzu.options.parse_command_line()
    application = anzu.web.Application()
    http_server = anzu.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
