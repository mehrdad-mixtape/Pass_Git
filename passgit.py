#!/bin/python3.8
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.8 or higher
# PassGit

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = "v1.0.0"

from packages import *

BANNER = f"""
    {PROJECT_NAME}
    Version: {__version__}
    Source: {__repo__}"""

passwd_path = f"{os.path.expanduser('~')}/{PASSWD_FILE}"
option = Options()

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

@option("-n", "--new")
def do_you_wanna_make_new_file() -> None:
    # .github_passwd.json exist but argv include -n
    if f"{PASSWD_FILE}" in os.listdir(f"{os.path.expanduser('~')}/"):
        pprint(
            f"[*] {WARNING}. {passwd_path} exist on your home dir!",
            f"\n  If you continue this operation your all Classic-Github-Token(passwd) will be [red]remove[/red]!",
            f"\n  Please make sure you have [cyan]backup[/cyan] and try again"
        )
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

    sys.exit()

@option('-a', '--add')
def do_you_wanna_add_new_passwd():
    with open(passwd_path, mode='r') as file:
        try:
            ciphers = json.load(file)
        except JSONDecodeError:
            pprint(f"[*] {ERROR}. {PASSWD_FILE} is corrupted! {HELP}")
            sys.exit()

    index = int(list(ciphers.keys()).pop())
    if index + 1 > MAX_PASSWD:
        with open(passwd_path, mode='w') as file:
            json.dump(ciphers, file)
            pprint(f"[*] {WARNING}. Maximum support passwd is {MAX_PASSWD}!")
            sys.exit()

    with open(passwd_path, mode='w') as file:
        aes = AESCipher(getpass.getpass('Give me your key: '))
        clear_passwd = getpass.getpass('Give me your new Classic-Github-Token(passwd): ')
        ciphers[index + 1] = aes.encrypt(clear_passwd).decode('utf-8')
        json.dump(ciphers, file)
        pprint(f"[*] {DEBUG}. New Classic-Github-Token(passwd) added '{passwd_path}'")

    pprint(f"[*] {INFO}. Do you wanna make [cyan]backup[/cyan](Y/N)? (default = N)", end='')
    answer = input()
    if answer in 'yY':
        backup(passwd_path, passwd_path + '.bkup')
        pprint(f"[*] {INFO}. Backup created {passwd_path} --> {passwd_path}.bkup")

    sys.exit()

@option('-d', '--dump')
def do_you_wanna_dump_passwd():
    with open(passwd_path, mode='r') as file:
        try:
            ciphers = json.load(file)
            for k, v in ciphers.items():
                pprint(f"{k}: {v}")
        except JSONDecodeError:
            pprint(f"[*] {ERROR}. {PASSWD_FILE} is corrupted! {HELP}")

    sys.exit()

@option('-b', '--backup')
def do_you_wanna_make_backup():
    backup(passwd_path, passwd_path + '.bkup')
    pprint(f"[*] {INFO}. Backup created {passwd_path} --> {passwd_path}.bkup")
    sys.exit()

@option('-g', '--give', has_args=True, limit_of_args=3)
def do_you_wanna_return_passwd(index):
    # $ passgit <1-20>
    aes = AESCipher(getpass.getpass('[*] Give me your key: '))
    try:
        with open(passwd_path, mode='r') as file:
            cipher_passwd = json.load(file).get(index, 'null')
            clear_passwd = aes.decrypt(cipher_passwd)
            copy(clear_passwd)
            pprint(f"[*] {INFO}. Classic-Github-Token(passwd) copied on clipboard!")
    except JSONDecodeError:
        pprint(f"[*] {ERROR}. {PASSWD_FILE} is corrupted! {HELP}")

    sys.exit()

def main() -> None:
    do_you_wanna_make_new_file()
    do_you_wanna_add_new_passwd()
    do_you_wanna_dump_passwd()
    do_you_wanna_make_backup()
    do_you_wanna_return_passwd()
    if sys.argv[1] not in option.option_list:
        pprint(BANNER)
        goodbye(True, cause=f"Invalid Switch [bold]{sys.argv[1]}[/bold]")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as err:
        pprint(f"\n[*] {ERROR}. Ctrl+C")
