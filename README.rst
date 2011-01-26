=============
wmark/anzu
=============
:Info: See `github <http://github.com/wmark/anzu>`_ for the latest source.
:Author: W-Mark Kubacki <wmark@hurrikane.de>

About
=====

Key differences to vanilla Tornado
----------------------------------

- Supports `non-regex handlers`, which are plain strings in a dictionary, what reduces the overhead for requests compared to matching regular expressions.
- Localization is based upon the standard `Gettext <http://www.gnu.org/software/gettext/>`_ instead of the CSV implementation in the original Tornado. Moreover, it supports pluralization exactly like Tornado does. By `Alexandre Fiori <fiorix@gmail.com>`_.
- Templating is done by `Mako <http://www.makotemplates.org/>`_, which features everything that the original templating module could (including compiling into native Python modules) and which has mature error reporting functions.
- Validation by `FormEncode <http://formencode.org/>`_ with decorators similar to TurboGears'.
- If ``dev-python/murmur`` is installed, static files will be hashed by `Murmurhash2 <http://murmurhash.googlepages.com/>`_ and not SHA1 or MD5.
- Sessions support from `Milan Cermak <http://github.com/milancermak/tornado/>`_. You can store session data in files, MySQL, Redis, Memcached and MongoDB.
- Runs under Windows, changes by `Mark Guagenti <http://github.com/mgenti/tornado>`_.
- Has `Location` and `Path` decorators, courtesy of Jeremy Kelley, Peter Bengtsson et al.

Example
========

::

    import anzu.httpserver
    import anzu.ioloop
    import anzu.web

    @anzu.web.location('/')
    class MainHandler(anzu.web.RequestHandler):
        def get(self):
            self.write("Hello, world")

    @anzu.web.path(r'/(\w+)')
    class SecondHandler(anzu.web.RequestHandler):
        def get(self, name):
            self.write("Hello, %s" % name)

    if __name__ == "__main__":
        cwd = os.path.dirname(__file__)
        application = anzu.web.Application()
        http_server = anzu.httpserver.HTTPServer(application)
        http_server.listen(8888)
        anzu.ioloop.IOLoop.instance().start()

`Location`s are being looked up first.

Please see the `demos` folder for more examples.

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
