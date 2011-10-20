#!/usr/bin/env python
import unittest

TEST_MODULES = [
    'anzu.httputil.doctests',
    'anzu.iostream.doctests',
    'anzu.util.doctests',
    'anzu.test.auth_test',
    'anzu.test.curl_httpclient_test',
    'anzu.test.escape_test',
    'anzu.test.gen_test',
    'anzu.test.httpclient_test',
    'anzu.test.httpserver_test',
    'anzu.test.httputil_test',
    'anzu.test.import_test',
    'anzu.test.ioloop_test',
    'anzu.test.iostream_test',
    'anzu.test.process_test',
    'anzu.test.simple_httpclient_test',
    'anzu.test.stack_context_test',
    'anzu.test.template_test',
    'anzu.test.testing_test',
    'anzu.test.twisted_test',
    'anzu.test.web_test',
    'anzu.test.wsgi_test',
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import anzu.testing
    anzu.testing.main()
