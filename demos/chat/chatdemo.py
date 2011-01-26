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

import logging
import anzu.auth
import anzu.escape
import anzu.ioloop
import anzu.options
import anzu.web
import os.path
import uuid

from anzu.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key",
       default="9e2ada1b462142c4dfcc8e894ea1e37c")
define("facebook_secret", help="your Facebook application secret",
       default="32fc6114554e3c53d5952594510021e2")
define("twitter_consumer_key", help="your twitter application consumer key",
       default="JqG2wwxuLK3oMpWhEpSl8g")
define("twitter_consumer_secret", help="your twitter application consumer secret",
       default="pyHRZWMSAEpmgSzbwZfHAyrHm0Cq9raJZR8H105mn8")



class Application(anzu.web.Application):
    def __init__(self):
        trivial_handlers = {
            "/": MainHandler,
            "/auth/login": AuthLoginHandler,
            "/auth/logout": AuthLogoutHandler,
            "/a/message/new": MessageNewHandler,
            "/a/message/updates": MessageUpdatesHandler,
        }
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            facebook_api_key=options.facebook_api_key,
            facebook_secret=options.facebook_secret,
            twitter_consumer_key=options.twitter_consumer_key,
            twitter_consumer_secret=options.twitter_consumer_secret,
        )
        anzu.web.Application.__init__(self, trivial_handlers=trivial_handlers, **settings)


class BaseHandler(anzu.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return anzu.escape.json_decode(user_json)


class MainHandler(BaseHandler):
    @anzu.web.authenticated
    def get(self):
        self.render("index.html", messages=MessageMixin.cache)


class MessageMixin(object):
    waiters = []
    cache = []
    cache_size = 200

    def wait_for_messages(self, callback, cursor=None):
        cls = MessageMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor: break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.waiters.append(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        logging.info("Sending new message to %r listeners", len(cls.waiters))
        for callback in cls.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = []
        cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]


class MessageNewHandler(BaseHandler, MessageMixin):
    @anzu.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["username"],
            "body": self.get_argument("body"),
        }
        message["html"] = self.render_string("message.html", message=message)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        self.new_messages([message])


class MessageUpdatesHandler(BaseHandler, MessageMixin):
    @anzu.web.authenticated
    @anzu.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.async_callback(self.on_new_messages),
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))


class AuthLoginHandler(BaseHandler, anzu.auth.GoogleMixin):
    @anzu.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token",self.get_argument("session", self.get_argument("openid.mode",None))): # oauth_token for twitter, session for facebook, openid_mode...
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(ax_attrs=["name"])

    def _on_auth(self, user):
        if not user:
            raise anzu.web.HTTPError(500, "Auth failed")
        self.set_secure_cookie("user", anzu.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        if not self.current_user:
            self.redirect(self.get_argument("next", "/"))
            return
        self.write("You are now logged out")


def main():
    anzu.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
