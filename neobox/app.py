from nemcore.api import NetEaseApi
from urwid import MainLoop, connect_signal, Padding, Filler, Overlay, Text, SolidFill, CENTER, MIDDLE

from neobox import config
from neobox.ui import layout, loginbox


class Application:

    def __init__(self):
        self.api = NetEaseApi(cookie_path=config.COOKIE_PATH, cache_path=config.REQUEST_CACHE_PATH)
        if self.api.profile:
            self.toplevel = layout.build()
        else:
            login_box = loginbox.LoginBox(self.api)
            self.toplevel = Padding(Filler(login_box), width=('relative', 20))
            connect_signal(login_box, 'login', self.on_login)
            connect_signal(login_box, 'api-error', self.on_error)

        self.loop = MainLoop(self.toplevel)

    def on_error(self, widget):
        backup = self.toplevel
        self.toplevel = Overlay(Padding(Filler(Text(f'{widget}'))),
                                SolidFill('/'),
                                CENTER, ('relative', 20),
                                MIDDLE, ('relative', 15))
        self.loop.widget = self.toplevel

    def on_login(self, widget):
        self.toplevel = layout.build()

    def run(self):
        self.loop.run()
