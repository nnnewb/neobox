from urwid import Columns

from neobox.ui import user


def build():
    return Columns([user.build()])
