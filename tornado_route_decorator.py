class route(object):
    """
    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or "What the *@# is really happening here?")
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

    my_routes = route.get_routes()
    """
    _routes = []

    def __init__(self, uri):
        self._uri = uri

    def __call__(self, _handler):
        """gets called when we class decorate"""
        self._routes.append((self._uri, _handler))
        return _handler

    @classmethod
    def get_routes(self):
        return self._routes

# route_redirect decorator provided by Peter Bengtsson via the Tornado mailing list.
# Use it as follows to redirect other paths into your decorated handler.
#
#   from routes import route, route_redirect
#   route_redirect('/smartphone$', '/smartphone/')
#   route_redirect('/iphone/$', '/smartphone/iphone/')
#   @route('/smartphone/$')
#   class SmartphoneHandler(RequestHandler):
#        def get(self):
#            ...

import tornado.web
def any_get_redirect(self, *a, **k):
    self.redirect(self.redirect_to)

def route_redirect(from_, to):
    created_handler = type('CustomRedirectHandler', (tornado.web.RequestHandler,),
                           dict(get=any_get_redirect))
    created_handler.redirect_to = to
    route._routes.append((from_, created_handler))


