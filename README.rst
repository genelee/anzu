=============
wmark/tornado
=============
:Info: See `github <http://github.com/wmark/tornado>`_ for the latest source.
:Author: W-Mark Kubacki <wmark@hurrikane.de>

About
=====

Key differences to vanilla Tornado
----------------------------------

- Supports `non-regex handlers`, which are plain strings in a dictionary, what reduces the overhead for requests compared to matching regular expressions.
- Localization is based upon the standard `Gettext <http://www.gnu.org/software/gettext/>`_ instead of the CSV implementation in the original Tornado. Moreover, it supports pluralization exactly like Tornado does.
- Templating is done by `Mako <http://www.makotemplates.org/>`_, which features everything that the original templating module could (including compiling into native Python modules) and which has a mature error reporting functions.
- Static files are hashed by `Murmurhash2 <http://murmurhash.googlepages.com/>`_ and not SHA1.

Extended Example
================
<pre><code>
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.locale

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # you don't need following line in templates
        _ = self.locale.translate
        self.write(_("Hello, world"))

class SecondHandler(tornado.web.RequestHandler):
    def get(self, name):
        # you don't need following line in templates
        _ = self.locale.translate
        self.write(_("Hello, %s") % name)

trivial_handlers = {
    "/": MainHandler,
}
handlers = [
    (r"/(\w+)", SecondHandler),
]
application = tornado.web.Application(
    handlers=handlers, trivial_handlers=trivial_handlers
)

if __name__ == "__main__":
    cwd = os.path.dirname(__file__)
    tornado.locale.load_translations(os.path.join(cwd, "locales"), "messages")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
</code></pre>

`trivial_handlers` are being looked up first.

Tornado
=======
Tornado is an open source version of the scalable, non-blocking web server
and and tools that power FriendFeed. Documentation and downloads are
available at http://www.tornadoweb.org/

Tornado is licensed under the Apache Licence, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0.html).

Installation
============
To install:

    python setup.py build
    sudo python setup.py install

Tornado has been tested on Python 2.5 and 2.6. To use all of the features
of Tornado, you need to have PycURL and a JSON library like simplejson
installed.

On Mac OS X, you can install the packages with:

    sudo easy_install setuptools pycurl==7.16.2.1 simplejson

On Ubuntu Linux, you can install the packages with:

    sudo apt-get install python-pycurl python-simplejson
