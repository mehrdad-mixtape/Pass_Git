#!/bin/python3.8
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.8 or higher
# PassGit

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = "v0.2.0"

import os, sys, base64, hashlib, getpass, json
from json.decoder import JSONDecodeError
from shutil import copyfile as backup
from typing import List
from packages import *
from settings import *

BANNER = f"""
    {PROJECT_NAME}
    Version: {__version__}
    Source: {__repo__}"""

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
            pprint(f"[*] {ERROR}. Passwd not found!")
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
        pprint(f"[*] {ERROR}. Please use -n or --new to create the {passwd_path}")
        sys.exit()

    # I used argv!, goodbye argparse!
    if argv[1] == '-n' or argv[1] == '--new':
        # .github_passwd.json exist but argv include -n
        if f"{PASSWD_FILE}" in os.listdir(f"{os.path.expanduser('~')}/"):
            pprint(f"[*] {WARNING}. {passwd_path} exist on your home dir!")
            pprint(f"[*] {WARNING}. If you continue this operation your all Classic-Github-Token(passwd) will be [red]remove[/red]!")
            pprint(f"[*] {WARNING}. Please make backup with -b --backup and run -n --new again")
            pprint(f"[*] {DEBUG}. Press [cyan]Ctrl+C[/cyan] to exit, or Press [yellow]Enter[/yellow] to continue ", end='')
            input()

        aes = AESCipher(getpass.getpass('[*] Give me your key: '))
        clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')

        with open(passwd_path, mode='w') as file:
            cipher_passwd = {
                1: aes.encrypt(clear_passwd).decode('utf-8')
            }
            json.dump(cipher_passwd, file)
            pprint(f"[*] {INFO}. Classic-Github-Token(passwd) stored in '{passwd_path}'")

    elif argv[1] == '-a' or argv[1] == '--add':
        with open(passwd_path, mode='r') as file:
            try:
                ciphers = json.load(file)
            except JSONDecodeError:
                pprint(f"[*] {ERROR}. {PASSWD_FILE} is corrupted! {OPTIONS}")

        index = int(list(ciphers.keys()).pop())
        if index + 1 > MAX_PASSWD:
            with open(passwd_path, mode='w') as file:
                json.dump(ciphers, file)
                pprint(f"[*] {WARNING}. Maximum support passwd is {MAX_PASSWD}!")

        with open(passwd_path, mode='w') as file:
            aes = AESCipher(getpass.getpass('Give me your key: '))
            clear_passwd = getpass.getpass('Give me your new Classic-Github-Token(passwd): ')
            ciphers[index + 1] = aes.encrypt(clear_passwd).decode('utf-8')
            json.dump(ciphers, file)
            pprint(f"[*] {DEBUG}. New Classic-Github-Token(passwd) added '{passwd_path}'")

    elif argv[1] == '-d' or argv[1] == '--dump':
        with open(passwd_path, mode='r') as file:
            try:
                ciphers = json.load(file)
                for k, v in ciphers.items():
                    pprint(f"{k}: {v}")
            except JSONDecodeError:
                pprint(f"[*] {ERROR}. {PASSWD_FILE} is corrupted! {OPTIONS}")
    
    elif argv[1] == '-b' or argv[1] == '--backup':
        backup(passwd_path, passwd_path + '.bkup')
        pprint(f"[*] {INFO}. Backup created {passwd_path} --> {passwd_path}.bkup")


    # $ passgit <1-20>
    elif argv[1] in ' '.join(map(str, [i for i in range(1, MAX_PASSWD + 1)])):
        index = argv[1]
        aes = AESCipher(getpass.getpass('[*] Give me your key: '))
        with open(passwd_path, mode='r') as file:
            cipher_passwd = json.load(file).get(index, 'null')
            clear_passwd = aes.decrypt(cipher_passwd)
            copy(clear_passwd)
            pprint(f"[*] {INFO}. Classic-Github-Token(passwd) copied on clipboard!")
    else:
        pprint(BANNER)
        pprint(OPTIONS)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt as err:
        pprint(f"\n[*] {ERROR}. Ctrl+C")
