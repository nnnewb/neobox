import click
import rich

from neobox.api import api


@click.command()
@click.argument('username', required=True, type=click.STRING, nargs=1)
@click.argument('password', required=True, type=click.STRING, nargs=1)
def login(username, password):
    """登录网易云音乐账号，支持邮箱和手机登录

    Args:
    
        username (str): 手机号或邮箱地址

        password (str): 密码
    """
    if not api.profile:
        api.login(username, password)
    rich.print(f'登录成功! [bold magenta]{api.profile.nickname}[/bold magenta]')
