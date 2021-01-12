from nemcore.api import NetEaseApi
from nemcore.exceptions import NetEaseError
from urwid import Edit, LineBox, Pile, Button, Filler, Padding, CENTER, connect_signal, emit_signal


class Login(LineBox):
    def __init__(self, api: NetEaseApi):
        self.username = ''
        self.password = ''
        self.api = api

        login_btn = Button('登录')
        username_edit = Edit('用户名: ')
        password_edit = Edit('密码: ', mask='*')

        connect_signal(username_edit, 'change', self.on_username_change)
        connect_signal(password_edit, 'change', self.on_password_change)
        connect_signal(login_btn, 'click', self.on_login_pressed)

        pile = Pile([])
        pile.contents.append((username_edit, pile.options()))
        pile.contents.append((password_edit, pile.options()))
        pile.contents.append((login_btn, pile.options()))

        super(Login, self).__init__(pile, title='请登录', title_align='left')

    def on_login_pressed(self, btn):
        try:
            resp = self.api.login(self.username, self.password)
            emit_signal(self, 'login', resp)
        except NetEaseError as e:
            pass

    def on_username_change(self, edit, text):
        self.username = text

    def on_password_change(self, edit, text):
        self.password = text
