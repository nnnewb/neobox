from nemcore.api import NetEaseApi as Api
from neobox import config

api = Api(cookie_path=config.cookies_path, cache_path=config.cache_path)
