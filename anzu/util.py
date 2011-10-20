"""Miscellaneous utility functions."""

class ObjectDict(dict):
    """Makes a dictionary behave like an object."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def import_object(name):
    """Imports an object by name.

    import_object('x.y.z') is equivalent to 'from x.y import z'.

    >>> import anzu.escape
    >>> import_object('anzu.escape') is anzu.escape
    True
    >>> import_object('anzu.escape.utf8') is anzu.escape.utf8
    True
    """
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1])

# Fake byte literal support:  In python 2.6+, you can say b"foo" to get
# a byte literal (str in 2.x, bytes in 3.x).  There's no way to do this
# in a way that supports 2.5, though, so we need a function wrapper
# to convert our string literals.  b() should only be applied to literal
# latin1 strings.  Once we drop support for 2.5, we can remove this function
# and just use byte literals.
if str is unicode:
    def b(s):
        return s.encode('latin1')
    bytes_type = bytes
else:
    def b(s):
        return s
    bytes_type = str

def doctests():
    import doctest
    return doctest.DocTestSuite()

#
# Copyright 2009-2010 W-Mark Kubacki; wmark@hurrikane.de
#

base_representation_chars = "0123456789abcdefghijklmnopqrstuvwxyz"

def baseN(num, b):
    """Converts the unsigned integer 'num' into its string representation
    in positional numeral system with base 'b'.

    Use this to get a short string representation of an otherwise long
    integer, e.g. hashes.

    Examples::

        >>> baseN(300, 36)
        '8c'
        >>> baseN(300, 10)
        '300'
        >>> baseN(300, 16)
        '12c'
        >>> baseN(300, 8)
        '454'
        >>> baseN(300, 5)
        '2200'
        >>> baseN(300, 2)
        '100101100'
        >>> baseN(0, 14)
        '0'
        >>> n = 2189753199
        >>> baseN(n, 36)
        '107q0dr'
        >>> n
        2189753199
    """
    assert num >= 0, "'num' must be positive"
    assert 0 < b <= len(base_representation_chars), \
        "radix 'b' must be greater than 0 and less or equal than 36"
    if num == 0:
        return "0"
    else:
        r = ''
        while num > 0:
            r += base_representation_chars[num % b]
            num = num // b
        return r[::-1]
