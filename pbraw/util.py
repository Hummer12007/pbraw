try:
    from urlib.parse import urlparse as _urlparse
    from urlib.parse import urlunparse as _urlunparse
except ImportError: #py2
    from urlparse import urlparse as _urlparse
    from urlparse import urlunparse as _urlunparse

urlparse = _urlparse
urlunparse = _urlunparse
