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

import anzu.auth
import anzu.escape
import anzu.httpserver
import anzu.ioloop
import anzu.options
import anzu.web

from anzu.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(anzu.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
        )
        anzu.web.Application.__init__(self, **settings)


class BaseHandler(anzu.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return anzu.escape.json_decode(user_json)


@anzu.web.location('/')
class MainHandler(BaseHandler):
    @anzu.web.authenticated
    def get(self):
        name = anzu.escape.xhtml_escape(self.current_user["name"])
        self.write("Hello, " + name)


@anzu.web.location('/auth/login')
class AuthHandler(BaseHandler, anzu.auth.GoogleMixin):
    @anzu.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise anzu.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", anzu.escape.json_encode(user))
        self.redirect("/")


def main():
    anzu.options.parse_command_line()
    http_server = anzu.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
