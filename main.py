import os
import re

import click
import pdbr
import rich
from nemcore.api import GetUserAccountResp, LoginResp
from nemcore.api import NetEaseApi as Api
from rich.table import Table
from rich.traceback import install

import config

install(show_locals=True)
api = Api(cookie_path=config.cookies_path, cache_path=config.cache_path)


@click.group()
def neobox():
    """ neobox 是一个网易云音乐的命令行客户端
    """
    pass


@neobox.command()
def clear_cache():
    """ 清除缓存

    注意会导致退出登录
    """
    os.remove(config.cookies_path)
    os.remove(config.cache_path)


@neobox.command()
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


@neobox.command(help='登出', short_help='登出')
def logout():
    pass


@neobox.command('list')
@click.option('--playlist')
def list_(playlist):
    """ 列出歌单或歌单内的歌曲。

    如果没有参数，列出所有播放列表。

    Args:

        playlist (str): 播放列表 ID 或名称
    """
    if playlist:
        tbl = Table(title='播放列表')
        tbl.add_column('ID')
        tbl.add_column('标题')
        tbl.add_column('专辑')
        tbl.add_column('歌手')
        tbl.add_column('时长')

        for track in api.get_playlist_detail(playlist).playlist.tracks:
            tbl.add_row(
                f'[bold green]{str(track.id)}[/bold green]',
                f'[bold magenta]{track.name}[/bold magenta]',
                track.al.name,
                ', '.join(map(lambda ar: ar.name, track.ar)),
                f'{int((track.dt/1000)/60)}分{int((track.dt/1000)%60)}秒',
            )
        
        rich.print(tbl)

    else:
        tbl = Table(title='播放列表')
        tbl.add_column('ID')
        tbl.add_column('标题')
        tbl.add_column('歌曲')
        tbl.add_column('收藏')
        tbl.add_column('播放')
        tbl.add_column('作者')

        for playlist in api.get_user_playlist().playlist:
            tbl.add_row(str(playlist.id), playlist.name,
                        str(playlist.track_count),
                        str(playlist.subscribed_count),
                        str(playlist.play_count), playlist.creator.nickname)

        rich.print(tbl)


@neobox.command('search', help='搜索歌曲', short_help='搜索歌曲')
def search():
    pass


@neobox.command(help='播放歌曲', short_help='播放歌曲')
def play():
    pass


@neobox.command(help='暂停播放', short_help='暂停播放')
def pause():
    pass


@neobox.command(help='停止播放', short_help='停止播放')
def stop():
    pass


if __name__ == "__main__":
    neobox()
