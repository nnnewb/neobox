from urwid.widget import FIXED, TOP
from neobox.ui.user import UserBox
from nemcore.api import NetEaseApi
from nemcore.exceptions import NetEaseError
from urwid import MainLoop, Columns, Pile, Text, WEIGHT, LineBox, Padding, Filler, CENTER, MIDDLE

from neobox import config
from neobox.ui.message_box import MessageBox
from neobox.ui.loginbox import LoginOverlay


class Application:
    def __init__(self):
        self.api = NetEaseApi(cookie_path=config.COOKIE_PATH,
                              cache_path=config.REQUEST_CACHE_PATH)

        self.loop = MainLoop(self.toplevel_widget())

        if not self.api.profile:
            LoginOverlay(self.loop, self.api).show()

    def toplevel_widget(self):
        left_pile = Pile([])
        left_pile.contents.append((UserBox(self.api), left_pile.options()))

        middle_pile = Pile([])
        middle_pile.contents.append((Text('TODO'), middle_pile.options()))

        right_pile = Pile([])
        right_pile.contents.append((Text('TODO'), right_pile.options()))

        columns = Columns([
            (WEIGHT, 1, left_pile),
            (WEIGHT, 2, middle_pile),
            (WEIGHT, 1, right_pile),
        ])

        return Filler(columns)

    def run(self):
        self.loop.run()
