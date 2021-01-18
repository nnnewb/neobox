import click
import rich
from rich.table import Table

from neobox.api import api


@click.command('list')
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
