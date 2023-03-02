import os, sys, base64, hashlib, getpass, json
from json.decoder import JSONDecodeError
from shutil import copyfile as backup, move as rename
from typing import List, Callable, Any, Dict, Tuple
from settings import *

PASSWD_PATH = f"{os.path.expanduser('~')}/{PASSWD_FILE}"

try:
    from rich.console import Console
    from rich.table import Table
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

def is_file_exist(file: str) -> bool:
    return file in os.listdir(f"{os.path.expanduser('~')}/")

def exception_handler(*exceptions, cause: str='', do_this: Callable=lambda: None) -> Callable[[Any], Any]:
    def __decorator__(func: Callable) -> Callable[[Any], Any]:
        def __wrapper__(*args, **kwargs) -> Any:
            try:
                results = func(*args, **kwargs)
            except exceptions as err:
                if cause:
                    pprint(f"\n[*] {ERROR}. {cause}")
                else:
                    pprint(f"\n[*] {err}")
                do_this()
                sys.exit()
            else:
                return results
        return __wrapper__
    return __decorator__

class AESCipher(object):
    def __init__(self, key: str): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw: str) -> str:
        raw = self.__pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode()

    @exception_handler(UnicodeDecodeError, ValueError, cause=f"Passwd not found!")
    def decrypt(self, enc: str) -> str:
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(enc[AES.block_size:])).decode()

    def __pad(self, s: str):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def __unpad(s: bytes):
        return s[:-ord(s[len(s)-1:])]

class Options:
    __slots__ = "__option_list", "__option_method"
    def __init__(self):
        self.__option_list: List[str] = []
        self.__option_method: Dict[str, Tuple[Callable, bool, int]] = {}

    def __str__(self):
        return f"List of options: {' '.join(self.__option_list)}"

    def __call__(self, *switches: str, has_input: bool=False):
        """
            switches: start with - or --.
            has_input: maybe the switches include the argument after them.
            limit_of_args: numbers of arguments after switches and depends on has_input.
        """
        self.__option_list.extend(switches)
        def __decorator__(func: Callable) -> Callable[[None], None]:
            for sw in switches:
                self[sw] = func.__name__

            @exception_handler(IndexError, cause=f"Not enough arguments after {' '.join(switches)}")
            def __wrapper__(loc_of_arg) -> Any:
                if not has_input:
                    return func()
                else:
                    return func(sys.argv[loc_of_arg])

            return __wrapper__
        return __decorator__

    def __setitem__(self, attr, value) -> None:
        self.__option_method[attr] = value

    def __getitem__(self, attr) -> Any:
        return self.__option_method[attr]

    @property
    def option_list(self) -> List[str]:
        return self.__option_list

    @property
    def option_method(self) -> Dict[str, str]:
        return self.__option_method
