#!/usr/bin/env python
#
# Copyright 2009 Facebook
# Copyright 2011 W-Mark Kubacki
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

# Changes to Tornado's demo:
# * Accepts WebSocket connections as well as long-polling.
# * Clients see messages of each other.

import logging
import anzu.auth
import anzu.escape
import anzu.ioloop
import anzu.options
import anzu.web
import anzu.websocket
import os.path
import uuid

from anzu.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(anzu.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            autoescape="xhtml_escape",
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
        self.render("index.html", messages=MessageMixin.cache)


class MessageMixin(object):
    waiters = set()
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
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MessageMixin
        if callback in cls.waiters:
            cls.waiters.remove(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        waiters = cls.waiters
        cls.waiters = set()
        logging.info("Sending new message to %r listeners", len(waiters))
        for callback in waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]


@anzu.web.location('/a/message/new')
class MessageNewHandler(BaseHandler, MessageMixin):
    @anzu.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["first_name"],
            "body": self.get_argument("body"),
        }
        message["html"] = self.render_string("message.html", message=message)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        self.new_messages([message])


@anzu.web.location('/a/message/updates')
class MessageUpdatesHandler(BaseHandler, MessageMixin):
    @anzu.web.authenticated
    @anzu.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.on_new_messages,
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_messages)


@anzu.web.location('/a/message/stream')
class MessagesWebSocket(BaseHandler, anzu.websocket.WebSocketHandler, MessageMixin):
    @anzu.web.authenticated
    def open(self):
        logging.debug("Socket opened by %s", self.current_user["first_name"])
        self.wait_for_messages(self.on_new_messages, cursor=None)

    def on_message(self, body): # from client
        logging.debug("Received a new message from %s: \"%s\"",
                      self.current_user["first_name"], body)
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["first_name"],
            "body": body,
        }
        message["html"] = self.render_string("message.html", message=message)
        self.new_messages([message])

    def on_new_messages(self, messages):
        if self.request.connection.stream.closed():
            return
        self.write_message(dict(messages=messages))
        self.wait_for_messages(self.on_new_messages, cursor=None)

    def on_connection_close(self):
        logging.debug("Connection to websocket has been closed by %s.", self.current_user["first_name"])
        self.cancel_wait(self.on_new_messages)


@anzu.web.location('/auth/login')
class AuthLoginHandler(BaseHandler, anzu.auth.GoogleMixin):
    @anzu.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(ax_attrs=["name"])

    def _on_auth(self, user):
        if not user:
            raise anzu.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("user", anzu.escape.json_encode(user))
        self.redirect("/")


@anzu.web.location('/auth/logout')
class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("You are now logged out")


def main():
    anzu.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    anzu.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
