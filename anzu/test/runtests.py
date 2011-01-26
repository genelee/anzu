#!/usr/bin/env python
import unittest

TEST_MODULES = [
    'anzu.httputil.doctests',
    'anzu.test.escape_test',
    'anzu.test.httpserver_test',
    'anzu.test.ioloop_test',
    'anzu.test.iostream_test',
    'anzu.test.simple_httpclient_test',
    'anzu.test.stack_context_test',
    'anzu.test.testing_test',
    'anzu.test.web_test',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import anzu.testing
    anzu.testing.main()
