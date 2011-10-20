#!/usr/bin/env python
#
# Copyright 2009 Facebook
# Copyright 2010 W-Mark Kubacki
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

import distutils.core
import sys
# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}

# Build the epoll extension for Linux systems with Python < 2.6
extensions = []
major, minor = sys.version_info[:2]
python_26 = (major > 2 or (major == 2 and minor >= 6))
if "linux" in sys.platform.lower() and not python_26:
    extensions.append(distutils.core.Extension(
        "anzu.epoll", ["anzu/epoll.c"]))

version = "2.1.1git"

if major >= 3:
    import setuptools  # setuptools is required for use_2to3
    kwargs["use_2to3"] = True

distutils.core.setup(
    name="anzu",
    version=version,
    packages = ["anzu", "anzu.test", "anzu.platform"],
    package_data = {
        "anzu": ["ca-certificates.crt"],
        "anzu.test": ["README.rst", "test.crt", "test.key", "static/robots.txt"],
        },
    ext_modules = extensions,
    author="W-Mark Kubacki",
    author_email="wmark+anzu@hurrikane.de",
    url="http://mark.ossdl.de/tags/anzu",
    download_url="http://github.com/downloads/wmark/anzu/anzu-%s.tbz2" % version,
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Fork of Facebook's Tornado with support for Mako templating, gettext i18n and sessions.",
    install_requires = [
        "Mako >= 0.2",
        "FormEncode >= 1.2.2",
    ],
    **kwargs
)
