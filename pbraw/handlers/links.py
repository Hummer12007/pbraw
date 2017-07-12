import lxml.html
import requests

from requests.exceptions import RequestException

from pbraw import dispatcher
from pbraw.util import urlparse, urlunparse
from pbraw.handlers.plain import grab_plain

@dispatcher.handler(priority=5)
def grab_from_links(url, req):
    if not req.headers['content-type'].startswith('text/html'):
        return False
    try:
        text = req.text
    except ValueError: # invalid encoding
        return False
    purl = list(urlparse(url))
    purl[3:5] = [''] * 3
    doc = lxml.html.document_from_string(text).make_links_absolute(urlunparse(purl))
    links = set()
    for el, attr, dest, pos in doc.getroot().iterlinks():
        if el.tag != 'a':
            continue
        for name in ['raw', 'download', 'plain']:
            if name in el.text_content().lower():
                purl.add(dest)
                break
    res = []
    for link in links:
        try:
            r = requests.get(link)
            r.raise_for_status()
        except RequestException:
            break
        ret = grab_plain(link)
        if ret:
            res.extend(ret)
    return res if res else False
