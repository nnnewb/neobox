import os
import random
from pathlib import Path
from queue import Empty, Queue
from threading import Thread

import click
import mad
import requests
import rich
import simpleaudio as sa
from rich.progress import BarColumn, Progress, TaskID, TotalFileSizeColumn

from neobox import config
from neobox.api import api


class CachingMusicFileTask:
    def __init__(self, progress: Progress, task_id: TaskID, url: str, local: str) -> None:
        super().__init__()
        self.progress = progress
        self.task_id = task_id
        self.url = url
        self.local = Path(local)

    @property
    def is_done(self):
        return self.local.exists()


class CachingMusicFile(Thread):
    def __init__(self, queue: Queue[CachingMusicFileTask]) -> None:
        super().__init__(name='caching-music-file', daemon=False)
        self.queue = queue

    def run(self) -> None:
        while True:
            try:
                task: CachingMusicFileTask = self.queue.get()
            except Empty:
                continue

            if task.is_done:
                task.progress.update(
                    task.task_id,
                    total=task.local.stat().st_size,
                    completed=task.local.stat().st_size
                )
                continue

            response = requests.get(task.url, stream=True)

            with task.local.open('wb+') as f:
                for chunk in response.iter_content(1024*100):
                    task.progress.update(task.task_id, advance=len(chunk))
                    f.write(chunk)


@click.command()
@click.option('--playlist', '-l', type=click.INT, nargs=1)
@click.option('--random-play', is_flag=True, default=False)
def play(playlist: int, random_play: bool):
    """播放歌单

    如果没有指定歌单id，默认播放名为 `我喜欢的音乐` 的歌单

    默认循环播放列表，可以使用 --random 选项来随机播放

    Args:
        playlist (int): 歌单id
        random (bool): 是否随机播放
    """
    if not playlist:
        user_playlist = api.get_user_playlist()
        for pl in user_playlist.playlist:
            if pl.name == '我喜欢的音乐':
                playlist = pl.id
                break

        if not playlist:
            rich.print('[red]没有找到播放列表')

    # start progress rendering in seprate thread immediately
    progress = Progress('[yellow]{task.fields[status]}[/yellow] '
                        '[progress.description]{task.description}',
                        '[blue]{task.fields[encode]}',
                        '[cyan]{task.fields[quality]}',
                        BarColumn(),
                        TotalFileSizeColumn(),
                        '[progress.percentage]{task.percentage:>3.0f}%',)
    Thread(target=progress.start, name='progress rendering').start()

    # initialize task queue
    task_queue: Queue[CachingMusicFileTask] = Queue(2)

    # initialize playtask
    play_task_id = progress.add_task('play', start=False, total=0, status='P', encode='-', quality='-')

    # start download threads
    thread_1 = CachingMusicFile(task_queue)
    thread_1.start()
    thread_2 = CachingMusicFile(task_queue)
    thread_2.start()

    # initialize tasks
    tasks = []
    tracks = api.get_playlist_detail(playlist).playlist.tracks
    tracks_id = list(map(lambda t: t.id, tracks))
    musics = api.get_songs_url(tracks_id, 0).data
    for track, music in zip(tracks, musics):
        music_cache_path = os.path.join(config.cache_folder, f'{track.id}.{music.type}')
        tasks.append(CachingMusicFileTask(progress,
                                          progress.add_task(f'{track.name}',
                                                            total=0,
                                                            encode=music.type,
                                                            quality=f'{music.br/1000}K',
                                                            status='D'),
                                          music.url,
                                          music_cache_path))

    # initialize download task queue
    def feed_taskq_queue():
        for task in tasks:
            task_queue.put(task)
    Thread(target=feed_taskq_queue, name='task producer').start()

    # start play
    local_musics = list(zip(tracks, musics))
    last_play_obj = None
    idx = 0
    while True:
        if random_play:
            track, music = random.choice(local_musics)
        else:
            if idx >= len(local_musics):
                idx = 0
            track, music = local_musics[idx]
            idx += 1

        local_path = os.path.join(config.cache_folder, f'{track.id}.{music.type}')
        progress.update(play_task_id, description=track.name)

        if Path(local_path).is_file():
            mf = mad.MadFile(Path(local_path).open('rb'))
            while True:
                buf = mf.read()
                if buf is None:
                    break

                if last_play_obj is not None and last_play_obj.is_playing():
                    last_play_obj.wait_done()

                last_play_obj = sa.play_buffer(buf, 2, 2, mf.samplerate())
