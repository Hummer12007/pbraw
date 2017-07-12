from os import path
import re

from pbraw import dispatcher
from pbraw.util import urlparse

CD_FILENAME_RE = re.compile('.*?;\s*filename\s*\*?\s*=\s*(?:\"(.*)\"\s*|(.*))', re.G, re.I, re.X)

@dispatcher.handler(priority=0)
def grab_plain(url, req):
    # TODO: properly implement RFC 6266 (Content-Disposition), 5987 (encodings)
    if req.headers['content-type'].startswith('text/html'):
        return False
    try:
        ret = req.text
    except ValueError: # invalid encoding
        return False
    if 'content-disposition' in req.headers:
        name = CD_FILENAME_RE.search(req.headers['content-disposition']) 
        if name: name = name.group(0)
    if not name:
        name = path.split(urlparse(url).path)
        if name: name = name[-1]
    if not name:
        name = urlparse(url).netloc # for the lack of a better name
    return [(name, ret)]
