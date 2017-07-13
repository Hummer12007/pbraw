from pbraw.dispatcher import URLDispatcher

dispatcher = URLDispatcher()

def grab(url):
    dispatcher.grab_url(url)

import pbraw.handlers
