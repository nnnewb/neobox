import typing

from urwid import (CENTER, MIDDLE, Button, Filler, LineBox, Pile, MainLoop,
                   Overlay, Padding, Text)

from .sizing import RELATIVE_15, RELATIVE_20


class MessageBox(Overlay):
    def __init__(self, loop: MainLoop, message: typing.Text):
        """
        A message box.
        """
        self.loop = loop
        self.background = loop.widget

        pile = Pile([])
        btn = Button('OK', self.close)
        pile.contents.append((Text(message, CENTER), pile.options()))
        pile.contents.append((btn, pile.options()))
        pile.focus_position = 1

        self.foreground = LineBox(Padding(Filler(pile), CENTER))

        super().__init__(self.foreground, self.background, CENTER, RELATIVE_20,
                         MIDDLE, RELATIVE_15)

    def close(self, *args):
        self.loop.widget = self.background

    def show(self):
        """
        show message box.
        """
        self.loop.widget = self

    @staticmethod
    def open(loop: MainLoop, message: typing.Text):
        """
        open a message box and wait user confirm.
        """
        return MessageBox(loop, message).show()
