#!/bin/python3
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.8 or higher
# PassGit

BETA = '-[red]alpha[/red]'
ALPHA = '-[purple]alpha[/purple]'
STABLE = '-[green]stable[/green]'

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = f"v1.6.5{STABLE}"

from packages import *

BANNER = f"""
---===❰ [blink]{PROJECT_NAME}[/blink] ❱===---
    Version: {__version__}
    Source: {__repo__}
"""

option = Options()

@option("-n", "--new")
def do_you_wanna_make_new_file() -> None:
    if is_file_exist(PASSWD_FILE):
        pprint(
            f"[{WARNING}]. {PASSWD_FILE} exist on your home dir!",
            f"\n  If you continue this operation your all Classic-Github-Token(passwd) will be [red]remove[/red]!",
            f"\n  Please make sure you have [cyan]backup[/cyan] and try again"
        )
        pprint(f"[{NOTICE}]. Press [cyan]Ctrl+C[/cyan] to exit, or Press [yellow]Enter[/yellow] to continue ", end='')
        input()

    aes = AESCipher(getpass.getpass('[*] (-n --new) Give me your key: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')

    for path in (PASSWD_PATH, f"{PASSWD_PATH}.bkup"):
        with open(path, mode='w') as file:
            cipher_passwd = {
                1: aes.encrypt(clear_passwd)
            }
            json.dump(cipher_passwd, file)
    pprint(f"[{INFO}]. Classic-Github-Token(passwd) stored in '{PASSWD_PATH}'")

@option('-a', '--add')
def do_you_wanna_add_new_passwd() -> None:
    with open(PASSWD_PATH, mode='r') as file:
        ciphers = json.load(file)

    index = int(list(ciphers.keys()).pop())
    if index + 1 > MAX_PASSWD:
        pprint(f"[{WARNING}]. Maximum support passwd is {MAX_PASSWD}!")
        sys.exit()

    aes = AESCipher(getpass.getpass('[*] (-a --add) Give me your key: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')
    ciphers[index + 1] = aes.encrypt(clear_passwd)

    with open(PASSWD_PATH, mode='w') as file:
        json.dump(ciphers, file)

    pprint(f"[{NOTICE}]. New Classic-Github-Token(passwd) added '{PASSWD_PATH}'")
    pprint(f"[{INFO}]. Do you wanna make [cyan]backup[/cyan](Y/N)? (default = N) ", end='')
    answer = input()

    if answer == 'y' or answer == 'Y':
        backup(PASSWD_PATH, f"{PASSWD_PATH}.bkup")
        pprint(f"[{INFO}]. Backup created {PASSWD_PATH} ❱❱❱ {PASSWD_PATH}.bkup")

@option('-d', '--dump')
def do_you_wanna_dump_passwd() -> None:
    with open(PASSWD_PATH, mode='r') as file:
        ciphers = json.load(file)
        table = Table()
        table.add_column('Access [blue]Index[/blue]')
        table.add_column(f"{ALGO} Cipher")
        for k, v in ciphers.items():
            table.add_row(f"  ❱❱ [blue]{k}[/blue] ❰❰", f"{v}")
        pprint(table)

@option('-b', '--backup')
def do_you_wanna_make_backup() -> None:
    if not is_file_exist(PASSWD_FILE_BKUP):
        backup(PASSWD_PATH, PASSWD_PATH + '.bkup')
        pprint(f"[{INFO}]. Backup created {PASSWD_PATH} ❱❱❱ {PASSWD_PATH}.bkup")
    else:
        pprint(f"[{WARNING}]. {PASSWD_PATH}.bkup exist on your home dir!")

@option('-r', '--restore')
def do_you_wanna_restore_backup() -> None:
    if is_file_exist(PASSWD_FILE_BKUP):
        if is_file_exist(PASSWD_FILE):
            pprint(
                f"[{WARNING}]. <{PASSWD_FILE}> exist in your home dir!",
                f"\n  If you continue this operation, <{PASSWD_FILE_BKUP}> will replace on <{PASSWD_FILE}>"
            )
            pprint(f"[{NOTICE}]. Press [cyan]Ctrl+C[/cyan] to exit, or Press [yellow]Enter[/yellow] to continue ", end='')
            input()
        os.remove(PASSWD_PATH)
        rename(f"{PASSWD_PATH}.bkup", PASSWD_PATH)
        pprint(f"[{INFO}]. Backup restored {PASSWD_PATH}.bkup ❱❱❱ {PASSWD_PATH}")
    else:
        pprint(f"[{WARNING}]. {PASSWD_PATH}.bkup don't exist on your home dir!")

@option('-g', '--give', has_input=True, type_of_input=str)
@exception_handler(PyperclipException, cause='Cannot forward clipboard in remote-Xsession, use -X in ssh sessions')
def do_you_wanna_return_passwd(index: str) -> None:
    with open(PASSWD_PATH, mode='r') as file:
        cipher_list = json.load(file)
        goodbye(
            index not in map(type(index), cipher_list.keys()),
            cause=f"Passwd not found with index={index}, use -d --dump to see",
            silent=True
        )
        cipher_passwd = cipher_list.get(index, 'null')
        aes = AESCipher(getpass.getpass('[*] (-g --give) Give me your key: '))
        clear_passwd = aes.decrypt(cipher_passwd)
        clipboard(clear_passwd)
        pprint(f"[{INFO}]. Classic-Github-Token(passwd) copied on clipboard!")

@option('-l', '--list')
def do_you_wanna_show_list_file() -> None:
    table = Table()
    table.add_column('Available [yellow]Files[/yellow]')
    for file in (PASSWD_FILE, PASSWD_FILE_BKUP):
        if is_file_exist(file):
            table.add_row(f"❱❱ <{file}> ❰❰")
    pprint(table)

@option('-h', '--help')
def do_you_wanna_help() -> None:
    pprint(HELP)

@exception_handler(KeyboardInterrupt, cause="Ctrl+C")
@exception_handler(JSONDecodeError, cause=f"<{PASSWD_FILE}> is corrupted!")
@exception_handler(IndexError, cause="Not enough arguments")
@exception_handler(FileNotFoundError, cause=f"<{PASSWD_FILE}> not found! if you have backup, restore it")
def main() -> None:
    pprint(BANNER)
    goodbye(
        len(sys.argv) == 1,
        cause='Not to use [bold]Switches[/bold]'
    )
    for _ in option.parse(): ...

if __name__ == '__main__':
    main()
