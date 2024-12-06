import os
import sys
import json
import time
import base64
import shutil
import hashlib
import getpass
import inspect
import datetime
import itertools
import dataclasses
from typing import (
    List, Tuple, Iterable, Any,Dict, NewType,
    Union, Generator, Callable, NewType
)
from json import JSONDecodeError
try:
    from Crypto import Random
    from Crypto.Cipher import AES

    import rich
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.box import HORIZONTALS
    from rich.progress import Progress
    from rich.style import Style
    from rich import print_json
    from rich import pretty, traceback
    from rich.markdown import Markdown

    pretty.install()
    traceback.install()
    log_console = Console()

    from pyperclip import copy as clipboard, PyperclipException

except ModuleNotFoundError as E:
	clock = datetime.datetime.now().strftime('%H:%M:%S')
	print(f"| {clock} [ERROR]. {E}, Please install Requirements!")
	sys.exit()
