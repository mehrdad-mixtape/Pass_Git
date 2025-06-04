#!/bin/python3
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.10 or higher
# PassGit

BETA = '[red]alpha[/]'
ALPHA = '[purple]alpha[/]'
STABLE = '[green]stable[/]'

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = f"v2.0.0-{STABLE}"
__project__ = 'Passgit'

from packages.globalFunc import (
    is_file_exist, goodbye, press_any, pprint,
    AESCipher,
)
from packages.decorators import exception_handler
from packages.libs import (
    getpass, json, sys, shutil, os,
    PyperclipException, clipboard,
    JSONDecodeError,
    Table,
) 
from packages.options import Options
from packages.logger import logger

BANNER = f"""
    ────━━━━ [blink][gold1]{__project__}[/][/] ━━━━────
        Version: {__version__}
        Source: {__repo__}
"""

PASSWD_FILE = ".github_passwd.json"
PASSWD_FILE_BKUP = f"{PASSWD_FILE}.bkup"
PASSWD_PATH = f"{os.path.expanduser('~')}/{PASSWD_FILE}"
MAX_PASSWD = 20

ALGO = '[purple]A[/][cyan]E[/][yellow]S[/]'

CGT = '[dark_orange]Classic-Github-Token(passwd)[/]'

option = Options(
    __project__,
    intro=f"""
    Store your {CGT} in [blue]Encrypted[/] format on your local system!",
    Decrypt your {CGT} with your key",
    Encryption Algorithm is {ALGO}
    """,
    run_without_help=False
)

@option(
    "-n", "--new",
    help_description=f"passgit -n. Enter your passwd and encrypt it, then will make new <{PASSWD_FILE}> in your home directory."
)
def do_you_wanna_make_new_file() -> None:
    if is_file_exist(PASSWD_FILE):
        logger(
            f"{PASSWD_FILE} exist on your home dir!",
            f"If you continue this operation your all Classic-Github-Token(passwd) will be REMOVE!",
            f"Please make sure you have BACKUP and try again",
            severity=2
        )
        press_any(who=f"{__project__}: ")

    aes = AESCipher(getpass.getpass('[*] Give me your key for encryption: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')

    for path in (PASSWD_PATH, f"{PASSWD_PATH}.bkup"):
        with open(path, mode='w') as file:
            cipher_passwd = {
                1: aes.encrypt(clear_passwd)
            }
            json.dump(cipher_passwd, file)

    logger(f"Classic-Github-Token(passwd) stored in '{PASSWD_PATH}'")


@option(
    '-a', '--add',
    help_description=f"passgit -a. Add new passwd on <{PASSWD_FILE}>, passgit support maximum {MAX_PASSWD} passwd to encrypt and store."
)
def do_you_wanna_add_new_passwd() -> None:
    with open(PASSWD_PATH, mode='r') as file:
        ciphers = json.load(file)

    index = int(list(ciphers.keys()).pop())
    if index + 1 > MAX_PASSWD:
        logger(f"Maximum support passwd is {MAX_PASSWD}!", severity=2)
        sys.exit()

    aes = AESCipher(getpass.getpass('[*] Give me your key for encryption: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')
    ciphers[index + 1] = aes.encrypt(clear_passwd)

    with open(PASSWD_PATH, mode='w') as file:
        json.dump(ciphers, file)

    logger(f"New Classic-Github-Token(passwd) added '{PASSWD_PATH}'", severity=3)

    if press_any(who=f"{__project__}: ", typ='yn', msg="Do you wanna make BACKUP"):
        shutil.copy(PASSWD_PATH, f"{PASSWD_PATH}.bkup")
        logger(f"Backup created {PASSWD_PATH} >>> {PASSWD_PATH}.bkup")


@option(
    '-d', '--dump',
    help_description=f"passgit -d. Dump all passwd <{PASSWD_FILE}>."
)
def do_you_wanna_dump_passwd() -> None:
    with open(PASSWD_PATH, mode='r') as file:
        ciphers = json.load(file)
        table = Table()
        table.add_column('Access [blue]Index[/]')
        table.add_column(f"{ALGO} Cipher")
        for k, v in ciphers.items():
            table.add_row(f":: [blue]{k}[/] ::", f"{v[0:30]} ...")

        pprint(table)


@option(
    '-b', '--backup',
    help_description=f"passgit -b. Make backup from <{PASSWD_FILE}>.bkup on home directory."
)
def do_you_wanna_make_backup() -> None:
    if not is_file_exist(PASSWD_FILE_BKUP):
        shutil.copy(PASSWD_PATH, PASSWD_PATH + '.bkup')
        logger(f"Backup created {PASSWD_PATH} >>> {PASSWD_PATH}.bkup")

    else:
        logger(f"{PASSWD_PATH}.bkup exist on your home dir!", severity=3)


@option(
    '-r', '--restore',
    help_description=f"passgit -r. Restore your backup from <{PASSWD_FILE}>.bkup to <{PASSWD_FILE}>."
)
def do_you_wanna_restore_backup() -> None:
    if not is_file_exist(PASSWD_FILE_BKUP):
        logger(f"{PASSWD_PATH}.bkup don't exist on your home dir!", severity=1)

    if is_file_exist(PASSWD_FILE):
        logger(f"<{PASSWD_FILE}> exist in your home dir!")
        logger(f"If you continue this operation, <{PASSWD_FILE_BKUP}> will replace on <{PASSWD_FILE}>", severity=2)
        press_any(who=f"{__project__}: ")

    os.remove(PASSWD_PATH)
    shutil.move(f"{PASSWD_PATH}.bkup", PASSWD_PATH)
    logger(f"Backup restored {PASSWD_PATH}.bkup >>> {PASSWD_PATH}")


@option(
    '-g', '--give',
    has_input=True,
    type_input=int,
    help_description=f"passgit -g <1-{MAX_PASSWD}>. Enter your decrypted passwd by index number between 1 and {MAX_PASSWD}."
)
@exception_handler(PyperclipException, cause='Cannot forward clipboard in remote-Xsession, use -X in ssh sessions')
def do_you_wanna_return_passwd(index: str) -> None:
    with open(PASSWD_PATH, mode='r') as file:
        cipher_list = json.load(file)

        passwd_index = f"{index}"

        goodbye(
            passwd_index not in map(type(passwd_index), cipher_list.keys()),
            cause=f"Passwd not found with index={passwd_index}, use -d --dump to see",
        )
        cipher_passwd = cipher_list.get(passwd_index, 'null')

        aes = AESCipher(getpass.getpass('[*] Give me your key for decryption: '))
        clear_passwd = aes.decrypt(cipher_passwd)

        clipboard(clear_passwd)
        logger(f"Classic-Github-Token(passwd) copied on clipboard!")


@option(
    '-l', '--list',
    help_description="passgit -l. Show the list of available files in your home directory."
)
def do_you_wanna_show_list_file() -> None:
    table = Table()
    table.add_column('Available [yellow]Files[/yellow]')
    for file in (PASSWD_FILE, PASSWD_FILE_BKUP):
        if is_file_exist(file):
            table.add_row(f"<{file}>")
    pprint(table)


@option(
    '-v', '--version',
    help_description=f"passgit -v. Show version of {__project__}."
)
def do_you_wanna_see_version() -> None:
    pprint(BANNER)
    exit(0)


@exception_handler(KeyboardInterrupt, cause="Ctrl+C")
@exception_handler(JSONDecodeError, cause=f"<{PASSWD_FILE}> is corrupted!")
@exception_handler(FileNotFoundError, cause=f"<{PASSWD_FILE}> not found! if you have backup, restore it")
def main() -> None:
    for _ in option.parse(): ...


if __name__ == '__main__':
    main()
