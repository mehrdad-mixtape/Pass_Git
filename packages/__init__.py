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
