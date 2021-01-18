import os

import click

from neobox import config


@click.command()
def clear_cache():
    """ 清除缓存

    注意会导致退出登录
    """
    os.remove(config.cookies_path)
    os.remove(config.cache_path)
