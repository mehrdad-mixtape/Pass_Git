import os, sys, base64, hashlib, getpass, json
from json.decoder import JSONDecodeError
from shutil import copyfile as backup
from typing import List, Callable, Any
from settings import *

try:
    from rich.console import Console
    from rich import pretty, traceback
except ImportError:
    print("[*] Error. Please install 'rich' pkg.\n$ pip3 install rich")
else:
    pretty.install()
    traceback.install()
    pprint = lambda *args, **kwargs: Console().print(*args, **kwargs)

try:
    from pyperclip import copy
except ImportError:
    pprint("[*] Error. Please install pyperclip' pkg.\n$ pip3 install pyperclip")

try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError as E:
    pprint("[*] Error. Please install 'pycryptodome' pkg.\n$ pip3 install pycryptodome")

def goodbye(expression: bool, cause: str='Unknown'):
    if expression:
        pprint(HELP)
        pprint(f"[*] {ERROR}. {cause}")
        sys.exit()

class Options:
    def __init__(self):
        self.__option_list: List[str] = []
    def __call__(self, *switches: str, has_args: bool=False, limit_of_args: int=2):
        self.__option_list.extend(switches)
        """
            switches: start with - or --.
            has_args: maybe the switches include the argument after them.
            limit_of_args: numbers of arguments after switches and depends on has_args.
        """
        def __decorator__(func: Callable[[Any], Any]) -> Callable[[None], None]:
            def __wrapper__() -> Any:
                goodbye(
                    len(sys.argv) < limit_of_args,
                    cause=f"Numbers of arguments={len(sys.argv)} but {limit_of_args=}, They should be Equal"
                )
                for sw in switches:
                    if sys.argv[1] == sw:
                        if not has_args: return func()
                        else: return func(sys.argv[2])
            return __wrapper__
        return __decorator__

    @property
    def option_list(self) -> List[str]:
        return self.__option_list
