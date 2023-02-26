#!/bin/python3.8
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.8 or higher
# PassGit

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = "v0.1.2"

import os, sys, base64, hashlib, getpass, json
from json.decoder import JSONDecodeError
from typing import List

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
    pprint("[*] [red]Error[/red]. Please install pyperclip' pkg.\n$ pip3 install pyperclip")

try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError as E:
    pprint("[*] [red]Error[/red]. Please install 'pycryptodome' pkg.\n$ pip3 install pycryptodome")

PASSWD_FILE = ".github_passwd.json"
MAX_PASSWD = 20
INFO = f"""
    [blink][dark_orange]Passgit[/dark_orange][/blink]
    Version: {__version__}
    Source: {__repo__}"""

OPTIONS = f"""
Intro:
    Store your [dark_orange]Classic-Github-Token(passwd)[/dark_orange] in [blue]Encrypted[/blue] format on your local system!
    [green]Decrypt[/green] your [dark_orange]Classic-Github-Token(passwd)[/dark_orange] with your [red]key[/red]
    Encryption Algorithm is [purple]A[/purple][cyan]E[/cyan][yellow]S[/yellow]

Helps:
    [bold][red]-n --new[/red][/bold]: Get your passwd and encrypt it, then will make new [yellow]<{PASSWD_FILE}>[/yellow] in your home directory
        $ passgit -n
    [bold][green]-a --add[/green][/bold]: Add new passwd on [yellow]<{PASSWD_FILE}>[/yellow], passgit support maximum {MAX_PASSWD} passwd to encrypt and store
        $ passgit -a
    [bold][cyan]-d --dump[/cyan][/bold]: Dump all passwd [yellow]<{PASSWD_FILE}>[/yellow]
        $ passgit -d
    [bold][purple]passgit <1-{MAX_PASSWD}>[/purple][/bold]: Give you your decrypted passwd by index number between 1 and {MAX_PASSWD}
        $ passgit 1 // Give your the first stored passwd in [yellow]<{PASSWD_FILE}>[/yellow]
"""

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw) -> bytes:
        raw = self.__pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc) -> str:
        try:
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self.__unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        except (UnicodeDecodeError, ValueError):
            pprint('[*] [red]Error[/red]. Passwd not found!')
            sys.exit()

    def __pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s)-1:])]

def main(argv: List[str]) -> None:
    passwd_path = f"{os.path.expanduser('~')}/{PASSWD_FILE}"
    if len(argv) < 2:
        pprint(INFO)
        pprint(OPTIONS)
        sys.exit()
    
    if f"{PASSWD_FILE}" not in os.listdir(f"{os.path.expanduser('~')}/"):
        pprint(f"[*] [red]Error[/red]. Please use -n or --new to create the {passwd_path}")
        sys.exit()

    if argv[1] == '-n' or argv[1] == '--new':
        # TODO Check the home dir if github_passwd.json had been existed, Show the Warning!
        aes = AESCipher(getpass.getpass('[*] Give me your key: '))
        clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')
        with open(passwd_path, mode='w') as file:
            cipher_passwd = {
                1: aes.encrypt(clear_passwd).decode('utf-8')
            }
            json.dump(cipher_passwd, file)
            pprint(f"[*] [green]Info[/green]. Classic-Github-Token(passwd) stored in '{passwd_path}'")

    elif argv[1] == '-a' or argv[1] == '--add':
        with open(passwd_path, mode='r') as file:
            try:
                ciphers = json.load(file)
            except JSONDecodeError:
                pprint(f"[*] [red]Error[/red]. {PASSWD_FILE} is corrupted! {OPTIONS}")

        index = int(list(ciphers.keys()).pop())
        if index + 1 > MAX_PASSWD:
            with open(passwd_path, mode='w') as file:
                json.dump(ciphers, file)
                pprint(f"[*] [dark_orange]Warning[/dark_orange]. Maximum support passwd is {MAX_PASSWD}!")

        with open(passwd_path, mode='w') as file:
            aes = AESCipher(getpass.getpass('Give me your key: '))
            clear_passwd = getpass.getpass('Give me your new Classic-Github-Token(passwd): ')
            ciphers[index + 1] = aes.encrypt(clear_passwd).decode('utf-8')
            json.dump(ciphers, file)
            pprint(f"[*] [purple]Debug[/purple]. New Classic-Github-Token(passwd) added '{passwd_path}'")

    elif argv[1] == '-d' or argv[1] == '--dump':
        with open(passwd_path, mode='r') as file:
            try:
                ciphers = json.load(file)
                for k, v in ciphers.items():
                    pprint(f"{k}: {v}")
            except JSONDecodeError:
                pprint(f"[*] [red]Error[/red]. {PASSWD_FILE} is corrupted! {OPTIONS}")

    # $ passgit <1-20>
    elif argv[1] in ' '.join(map(str, [i for i in range(1, MAX_PASSWD + 1)])):
        index = argv[1]
        aes = AESCipher(getpass.getpass('[*] Give me your key: '))
        with open(passwd_path, mode='r') as file:
            cipher_passwd = json.load(file).get(index, 'null')
            clear_passwd = aes.decrypt(cipher_passwd)
            copy(clear_passwd)
            pprint('[*] [green]Info[/green]. Classic-Github-Token(passwd) copied on clipboard!')
    else:
        pprint(INFO)
        pprint(OPTIONS)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt as err:
        pprint(f"\n[*] [red]Error[/red]. Ctrl+C")
