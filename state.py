import config

from typing import List

from nemcore.api import NetEaseApi
from nemcore.types import Playlist


class Neobox:
    def __init__(self):
        self.user_playlists: List[Playlist] = []
        self.api = NetEaseApi(cookie_path=config.cookies_path,
                              cache_path=config.cache_path)
