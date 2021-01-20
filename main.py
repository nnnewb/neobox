from rich.traceback import install

from neobox.cli import neobox

install(show_locals=True)

if __name__ == "__main__":
    neobox()
