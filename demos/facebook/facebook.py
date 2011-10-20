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

import os.path
import anzu.auth
import anzu.escape
import anzu.httpserver
import anzu.ioloop
import anzu.options
import anzu.web

from anzu.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key",
       default="9e2ada1b462142c4dfcc8e894ea1e37c")
define("facebook_secret", help="your Facebook application secret",
       default="32fc6114554e3c53d5952594510021e2")


class Application(anzu.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            mako_module_directory='/tmp/mako_modules',
            ui_modules={"Post": PostModule},
            debug=True,
            autoescape=None,
        )
        anzu.web.Application.__init__(self, **settings)


class BaseHandler(anzu.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return anzu.escape.json_decode(user_json)


@anzu.web.location('/')
class MainHandler(BaseHandler, anzu.auth.FacebookGraphMixin):
    @anzu.web.authenticated
    @anzu.web.asynchronous
    def get(self):
        self.facebook_request("/me/home", self._on_stream,
                              access_token=self.current_user["access_token"])

    def _on_stream(self, stream):
        if stream is None:
            # Session may have expired
            self.redirect("/auth/login")
            return
        self.render("stream.html", stream=stream)


@anzu.web.location('/auth/login')
class AuthLoginHandler(BaseHandler, anzu.auth.FacebookGraphMixin):
    @anzu.web.asynchronous
    def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  anzu.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self._on_auth)
            return
        self.authorize_redirect(redirect_uri=my_url,
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "read_stream"})

    def _on_auth(self, user):
        if not user:
            raise anzu.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("user", anzu.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


@anzu.web.location('/auth/logout')
class AuthLogoutHandler(BaseHandler, anzu.auth.FacebookGraphMixin):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))


class PostModule(anzu.web.UIModule):
    def render(self, post):
        return self.render_string("modules/post.html", post=post)


def main():
    anzu.options.parse_command_line()
    http_server = anzu.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
