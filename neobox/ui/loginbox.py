from neobox.ui.sizing import RELATIVE_15, RELATIVE_20
from nemcore.api import NetEaseApi
from nemcore.exceptions import NetEaseError
from nemcore.types.login_resp import LoginResp
from urwid import Edit, LineBox, Pile, Button, connect_signal, emit_signal, Overlay, MainLoop, Padding, Filler, MIDDLE, CENTER, RELATIVE_100
from .message_box import MessageBox


class LoginBox(LineBox):
    """ 登录框

    可能抛出的 signal

    - ``login`` 表示登录成功
    - ``api-error`` 表示出现 Api 错误
    """
    signals = ['login', 'api-error']

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

        super(LoginBox, self).__init__(pile, title='请登录', title_align='left')

    def on_login_pressed(self, btn):
        try:
            resp = self.api.login(self.username, self.password)
            emit_signal(self, 'login', resp)
        except NetEaseError as e:
            emit_signal(self, 'api-error', e)

    def on_username_change(self, edit, text):
        self.username = text

    def on_password_change(self, edit, text):
        self.password = text


class LoginOverlay(Overlay):
    def __init__(self, loop: MainLoop, api: NetEaseApi):
        self.loop = loop
        self.login_box = LoginBox(api)
        self.foreground = Padding(Filler(self.login_box), CENTER)
        self.background = self.loop.widget
        super().__init__(self.foreground, self.background, CENTER, RELATIVE_20,
                         MIDDLE, RELATIVE_15)

        connect_signal(self.login_box, 'login', self.on_login)
        connect_signal(self.login_box, 'api-error', self.on_error)

    def on_error(self, *args):
        """
        on error occurred
        """
        error = args[0]
        MessageBox.open(
            self.loop,
            f'=== error occurred ===\ncode {error.code}\nmessage {error.message}'
        )

    def on_login(self, *args):
        """
        on login done
        """
        emit_signal(self, 'login', *args)
        self.close()

    def show(self):
        """
        show login overlay
        """
        self.loop.widget = self

    def close(self, *args):
        """
        close login overlay
        """
        self.loop.widget = self.background
