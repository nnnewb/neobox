from os.path import abspath, expanduser, join, exists, isdir
from os import makedirs, remove

cache_folder = join(abspath(expanduser('~')), '.cache', 'neobox')
if not exists(cache_folder):
    makedirs(cache_folder, 0o755, True)
elif not isdir(cache_folder):
    remove(cache_folder)
    makedirs(cache_folder, 0o755, True)

cookies_path = join(cache_folder, 'cookies')
cache_path = join(cache_folder, 'cache')
