#!/usr/bin/env python
#
# Copyright 2010 W-Mark Kubacki
#

import anzu.escape
import anzu.httpserver
import anzu.ioloop
import anzu.options
import anzu.web

from anzu.options import define, options
from anzu import validators

define("port", default=8888, help="run on the given port", type=int)


@anzu.web.location('/')
class MainHandler(anzu.web.RequestHandler):
    def get(self):
        if self.error_for('email'):
            message = '<font color="red">' + self.error_for('email') + '</font><br />'
        else:
            message = 'Please give us your email.'
        old_value = anzu.escape.xhtml_escape(self.get_argument("email", ''))
        self.write(
            message
            + '<form method="post">Email: <input type="text" name="email" value="'
            + old_value + '" />'
            + '<input type="submit" /></form>'
        )

    @validators.error_handler(get)
    @validators.validate(validators={'email': validators.Email(not_empty=True)})
    def post(self):
        self.write("Your email is <b>%s</b>." % self.get_argument("email"))


def main():
    anzu.options.parse_command_line()
    application = anzu.web.Application()
    http_server = anzu.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
