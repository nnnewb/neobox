import click
import rich
from rich.table import Table

from neobox.api import api


@click.command('search', help='搜索歌曲', short_help='搜索歌曲')
@click.argument('keywords')
def search(keywords: str):
    """搜索歌曲

    Args:
        keywords (str): 关键词，用逗号分割
    """
    search_keywords = ' '.join(keywords.split(','))
    tbl = Table(title=f'搜索结果')
    tbl.add_column('ID')
    tbl.add_column('标题')
    tbl.add_column('专辑')
    tbl.add_column('歌手')
    tbl.add_column('时长')

    for song in api.search(search_keywords).result.songs:
        tbl.add_row(
            f'[bold green]{song.id}[/bold green]',
            song.name,
            song.album.name,
            ', '.join(map(lambda ar: ar.name, song.artists)),
            f'{int((song.duration/1000)/60)}分{int((song.duration/1000)%60)}秒',
        )

    rich.print(tbl)
