from typing import Optional

import click
import rich
from rich.progress import Progress
from rich.table import Table

from neobox.api import api


@click.command()
@click.option('--playlist', '-l', type=click.INT, nargs=1)
def play(playlist: int):
    """播放歌单

    如果没有指定歌单id，默认播放名为 `我喜欢的音乐` 的歌单

    Args:
        playlist (int): 歌单id
    """
    if not playlist:
        user_playlist = api.get_user_playlist()
        for pl in user_playlist.playlist:
            if pl.name == '我喜欢的音乐':
                playlist = pl.id

    tbl = Table()
    tbl.add_column('ID')
    tbl.add_column('名称')
    tbl.add_column('类型')
    tbl.add_column('支付')
    tbl.add_column('费用')

    resp = api.get_playlist_detail(playlist)
    for track in resp.playlist.tracks:
        url_resp = api.get_songs_url([track.id], 0)
        for d in url_resp.data:
            tbl.add_row(str(d.id), track.name, d.type, str(d.payed),
                        str(d.fee))

    rich.print(tbl)
