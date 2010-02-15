#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import anzu.httpserver
import anzu.ioloop
import anzu.options
import anzu.web

from anzu.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(anzu.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def main():
    anzu.options.parse_command_line()
    application = anzu.web.Application(trivial_handlers={
        "/": MainHandler,
    })
    http_server = anzu.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
