from nemcore.api import NetEaseApi
from urwid import LineBox, ListBox, Button, Pile, SimpleFocusListWalker, Text, CENTER


class UserBox(LineBox):
    def __init__(self, api: NetEaseApi):
        nickname = Text(api.profile.nickname if api.profile else '** 未登录 **')

        pile = Pile([])
        self.widget = pile
        self.widget.contents.append((nickname, pile.options()))

        super().__init__(self.widget)
