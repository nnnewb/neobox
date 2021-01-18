import os
import re

import click
import pdbr
import rich
from nemcore.api import GetUserAccountResp, LoginResp
from nemcore.api import NetEaseApi as Api
from rich.table import Table
from rich.traceback import install
from neobox.cli import neobox

install(show_locals=True)

if __name__ == "__main__":
    neobox()
