from urwid import LineBox, ListBox, Button, Pile, SimpleFocusListWalker


def build():
    return LineBox(
        ListBox(SimpleFocusListWalker([
            Button('Hello')
        ])), '用户'
    )
