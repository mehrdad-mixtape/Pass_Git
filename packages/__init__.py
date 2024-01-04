import os, sys, base64, hashlib, getpass, json
from json.decoder import JSONDecodeError
from time import sleep
from shutil import copyfile as backup, move as rename
from typing import List, Callable, Any, Dict, Tuple, Generator
from settings import *

PASSWD_PATH = f"{os.path.expanduser('~')}/{PASSWD_FILE}"

try:
    from rich.console import Console
    from rich.table import Table
    from rich import pretty, traceback
except ImportError:
    print("[Error]. Please install 'rich' pkg.\n$ pip3 install rich")
else:
    pretty.install()
    traceback.install()
    pprint = lambda *args, **kwargs: Console().print(*args, **kwargs) if None not in args else ...

try:
    from pyperclip import copy as clipboard, PyperclipException
except ImportError:
    pprint("[Error]. Please install pyperclip' pkg.\n$ pip3 install pyperclip")

try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError as E:
    pprint("[Error]. Please install 'pycryptodome' pkg.\n$ pip3 install pycryptodome")

def goodbye(expression: bool, cause: str='Unknown'):
    if expression:
        pprint(f"[{ERROR}]. {cause}")
        sys.exit()

def is_file_exist(file: str) -> bool:
    return file in os.listdir(f"{os.path.expanduser('~')}/")

def exception_handler(*exceptions, cause: str='', do_this: Callable=sys.exit) -> Callable[[Any], Any]:
    def __decorator__(func: Callable) -> Callable[[Any], Any]:
        def __wrapper__(*args, **kwargs) -> Any:
            try:
                results = func(*args, **kwargs)
            except exceptions as err:
                if cause:
                    pprint(f"\n[{ERROR}]. {cause}")
                else:
                    pprint(f"\n[{ERROR}]. {err}")
                do_this()
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
    """
    Argument Parser!
    
    1. Make option object:
    
        option = Option()
    
    2. Assign function to option object:
    
        - Decorate function with option object
    
            @option('-s')

            def do_you_wanna_something_to_do():
                ...
            
            @option('--switch')

            def do_you_wanna_something_to_do():
                ...
            
            @option('-s', '--switch')

            def do_you_wanna_something_to_do():
                ...
            
            @option('-s', '--switch', has_input=True, type_of_input=type)

            def do_you_wanna_something_to_do(arg: type):
                ...
    
        - Directly

            option['- or -- switch'] = (function, has_input(True or False), type_of_input=(str, int, ...))

            option['-s'] = (do_you_wanna_something_to_do)
            
            option['-s'] = (do_you_wanna_something_to_do, True, type)

            option['--switch'] = (do_you_wanna_something_to_do)
            
            option['--switch'] = (do_you_wanna_something_to_do, True, type)
    """

    __slots__ = "__option_list", "__option_method"

    def __init__(self):
        self.__option_list: List[str] = []
        self.__option_method: Dict[str, Tuple[Callable[[Any], Any], bool, type]] = {}

    def __str__(self):
        table = Table()
        table.add_column('Switches')
        table.add_column('Methods')
        for switch, method in self.option_method.items():
            table.add_row(switch, method[0].__name__)
        pprint(table)
        return '\r'

    def __call__(
            self, *switches: str,
            has_input: bool=False,
            type_of_input: type=None
        ):
        """
            switches: start with - or --.
            has_input: maybe the switches include the argument after them.
            type_of_input: type of arguments after switch and depends on has_input.
        """
        def __decorator__(func: Callable[[Any], Any]) -> Callable[[None], None]:
            for sw in switches:
                goodbye(
                    sw in self.__option_method.keys(),
                    cause="Duplicate switch={0}, [bold]{1}[/bold] used for [bold]{2}[/bold]".format(
                        sw, sw, self.__option_method.get(sw, (print,))[0].__name__
                    )
                )
                self.__option_method[sw] = (func, has_input, type_of_input)

            self.__option_list.extend(switches)

        return __decorator__

    def __setitem__(self, key: str, value: tuple) -> None:
        goodbye(
            not ((not isinstance(value, tuple) or value.__len__() < 3) and callable(value[0])),
            cause="""Bad value format.\nValid format:
        option_obj['-s' or '--switch' or '-s --switch'] = (
            function, # Should be Callable.
            True or False, # If your function should get argument, set it True or not False.
            type, # Set type of argument that will pass to function (str, int, ...).
        )""",
        )
        self.__option_method[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.__option_method.get(key, None)

    def parse(self) -> Generator[Any, None, None]:
        for i, sw in enumerate(sys.argv, start=1):
            # goodbye(sw.startswith(('+', '=', '/', '\\', '$', '#', '>', '<', '@', '!', '`', '~')))

            if not sw.startswith(('-', '--')):
                continue # valid switches can start with - --            
            
            # Handle the complete-switches: Example ==> --add --list --dump
            if '--' in sw:
                yield self.__switch_executer(sw, i)
                continue
            
            # Handle the abbreviation-switches: Example ==> -a -l -d
            # Handle the mixed abbreviation-switches: Example ==> -ald = -dal
            for chr in sw:
                goodbye( # if user enter just -
                    sw.__len__() == 1,
                    cause=f"Invalid Switch=({sw})"
                )
                if chr == '-': continue
                e_sw = f"-{chr}" # esw = extracted_switch
                yield self.__switch_executer(e_sw, i)

    def __switch_executer(self, switch: str, switch_index: int) -> None:
        try:
            func, has_input, type_of_input = self.option_method[switch]
            # func is __wrapper__ in __call__ that defined in Options class
            # if switch has input, I should pass the location of input to func
            # if it hasn't, it will be handle in __wrapper__ with has_input
        except KeyError:
            goodbye(True, cause=f"Invalid Switch=({switch})")
        # eval(f"{func}({i + 1})")
        if not has_input:
            return func()
        else:
            arg_input = sys.argv[switch_index].__str__()
            goodbye(
                type_of_input is None,
                cause=f"Get type-of-arguments=({arg_input}) after [bold]{switch}[/bold]",
            )
            try:
                arg_input = type_of_input(arg_input)
            except ValueError:
                goodbye(
                    True,
                    cause=f"Gave bad-argument=({arg_input}) after [bold]{switch}[/bold]",
                )
            return func(arg_input)

    @property
    def option_list(self) -> List[str]:
        return self.__option_list

    @property
    def option_method(self) -> Dict[str, str]:
        return self.__option_method
