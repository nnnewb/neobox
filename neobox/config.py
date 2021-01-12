import os

cache_dir = os.path.expanduser('~/.cache/neobox')
if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)

COOKIE_PATH = os.path.expanduser('~/.cache/neobox/cookies')
REQUEST_CACHE_PATH = os.path.expanduser('~/.cache/neobox/request-cache')
