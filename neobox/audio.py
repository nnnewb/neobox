import sys
from threading import Thread


class InitializeFailError(Exception):
    pass


class PlaybackError(Exception):
    pass


try:
    import gi

    gi.require_version('Gst', '1.0')

    # GObject.MainLoop has deprecated
    from gi.repository import GLib, Gst

    # PyGIDeprecationWarning: Since version 3.11, calling threads_init is no longer needed. See: https://wiki.gnome.org/PyGObject/Threading
    # GObject.threads_init()
    Gst.init(None)

    # reference: https://github.com/GStreamer/gst-python/blob/master/examples/helloworld.py
    class AudioPlayer(Thread):
        """音频回放工具
        """

        def __init__(self):
            """音频回放工具

            Raises:
                InitializeFailError: playbin 初始化失败
            """
            self.loop = GLib.MainLoop()
            self.playbin = Gst.ElementFactory.make('playbin', None)
            if not self.playbin:
                raise InitializeFailError('playbin gstreamer plugin missing.')

            # setup bus callback
            self.bus = self.playbin.get_bus()
            self.bus.add_signal_watch()
            self.bus.connect("message", self.bus_call)

        def playback(self, uri: str):
            if not Gst.uri_is_valid(uri):
                uri = Gst.filename_to_uri(uri)

            self.playbin.set_property('uri', uri)

        def run(self) -> None:
            try:
                self.loop.run()
            except:
                raise

        def bus_call(self, msg):
            if msg.type == Gst.MessageType.EOS:
                sys.stdout.write("End-of-stream\n")
                self.loop.quit()
            elif msg.type == Gst.MessageType.ERROR:
                err, debug = msg.parse_error()
                sys.stderr.write("Error: %s: %s\n" % (err, debug))
                self.loop.quit()
            return True


except Exception as e:
    raise

if __name__ == "__main__":
    player = AudioPlayer()
    player.playback()
    player.run()
    player.join()
