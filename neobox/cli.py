import click

from neobox.cmd.list import list_
from neobox.cmd.clear_cache import clear_cache
from neobox.cmd.login import login
from neobox.cmd.logout import logout
from neobox.cmd.search import search
from neobox.cmd.play import play
from neobox.cmd.pause import pause
from neobox.cmd.stop import stop


@click.group()
def neobox():
    """ neobox 是一个网易云音乐的命令行客户端
    """
    pass


neobox.add_command(login)
neobox.add_command(logout)
neobox.add_command(list_)
neobox.add_command(search)
neobox.add_command(play)
neobox.add_command(pause)
neobox.add_command(stop)
neobox.add_command(clear_cache)
