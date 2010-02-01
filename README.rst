=============
wmark/tornado
=============
:Info: See `github <http://github.com/wmark/tornado>`_ for the latest source.
:Author: W-Mark Kubacki <wmark@hurrikane.de>

About
=====

Key differences to vanilla Tornado
----------------------------------

- Localization is based upon the standard `Gettext <http://www.gnu.org/software/gettext/>`_ instead of the CSV implementation in the original Tornado. Moreover, it supports pluralization exactly like Tornado does.
- Templating is done by `Mako <http://www.makotemplates.org/>`_, which features everything that the original templating module could (including compiling into native Python modules) and which has a mature error reporting functions.

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
