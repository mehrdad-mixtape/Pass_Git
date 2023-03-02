#!/bin/python3.8
# -*- coding: utf8 -*-

# MIT License

# Copyright (c) 2023 mehrdad
# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Pass_Git

# Python Version 3.8 or higher
# PassGit
# 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

BETA = '-[red]alpha[/red]'
ALPHA = '-[purple]alpha[/purple]'
STABLE = '-[green]stable[/green]'

__repo__ = "https://github.com/mehrdad-mixtape/Pass_Git"
__version__ = f"v2.4.1{STABLE}"

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
            f"[*] {WARNING}. {PASSWD_PATH} exist on your home dir!",
            f"\n  If you continue this operation your all Classic-Github-Token(passwd) will be [red]remove[/red]!",
            f"\n  Please make sure you have [cyan]backup[/cyan] and try again"
        )
        pprint(f"[*] {DEBUG}. Press [cyan]Ctrl+C[/cyan] to exit, or Press [yellow]Enter[/yellow] to continue ", end='')
        input()

    aes = AESCipher(getpass.getpass('[*] (-n --new) Give me your key: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')

    for path in (PASSWD_PATH, f"{PASSWD_PATH}.bkup"):
        with open(path, mode='w') as file:
            cipher_passwd = {
                1: aes.encrypt(clear_passwd)
            }
            json.dump(cipher_passwd, file)
    pprint(f"[*] {INFO}. Classic-Github-Token(passwd) stored in '{PASSWD_PATH}'")

@option('-a', '--add')
def do_you_wanna_add_new_passwd() -> None:
    with open(PASSWD_PATH, mode='r') as file:
        ciphers = json.load(file)

    index = int(list(ciphers.keys()).pop())
    if index + 1 > MAX_PASSWD:
        pprint(f"[*] {WARNING}. Maximum support passwd is {MAX_PASSWD}!")
        sys.exit()

    aes = AESCipher(getpass.getpass('[*] (-a --add) Give me your key: '))
    clear_passwd = getpass.getpass('[*] Give me your new Classic-Github-Token(passwd): ')
    ciphers[index + 1] = aes.encrypt(clear_passwd)

    with open(PASSWD_PATH, mode='w') as file:
        json.dump(ciphers, file)

    pprint(f"[*] {DEBUG}. New Classic-Github-Token(passwd) added '{PASSWD_PATH}'")
    pprint(f"[*] {INFO}. Do you wanna make [cyan]backup[/cyan](Y/N)? (default = N) ", end='')
    answer = input()

    if answer == 'y' or answer == 'Y':
        backup(PASSWD_PATH, f"{PASSWD_PATH}.bkup")
        pprint(f"[*] {INFO}. Backup created {PASSWD_PATH} ❱❱❱ {PASSWD_PATH}.bkup")

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
        pprint(f"[*] {INFO}. Backup created {PASSWD_PATH} ❱❱❱ {PASSWD_PATH}.bkup")
    else:
        pprint(f"[*] {WARNING}. {PASSWD_PATH}.bkup exist on your home dir!")

@option('-r', '--restore')
def do_you_wanna_restore_backup() -> None:
    if is_file_exist(PASSWD_FILE_BKUP):
        os.remove(PASSWD_PATH)
        rename(f"{PASSWD_PATH}.bkup", PASSWD_PATH)
        pprint(f"[*] {INFO}. Backup restored {PASSWD_PATH}.bkup ❱❱❱ {PASSWD_PATH}")
    else:
        pprint(f"[*] {WARNING}. {PASSWD_PATH}.bkup don't exist on your home dir!")

@option('-g', '--give', has_input=True)
def do_you_wanna_return_passwd(index) -> None:
    goodbye(
        not index.isdigit(),
        cause=f"Bad argument=({index}) after -g --give"
    )
    with open(PASSWD_PATH, mode='r') as file:
        aes = AESCipher(getpass.getpass('[*] (-g --give) Give me your key: '))
        cipher_passwd = json.load(file).get(index, 'null')
        clear_passwd = aes.decrypt(cipher_passwd)
        copy(clear_passwd)
        pprint(f"[*] {INFO}. Classic-Github-Token(passwd) copied on clipboard!")

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

@exception_handler(KeyError, cause='Invalid Switch, use passgit -h to show you the help')
def manage() -> None:
    for i, sw in enumerate(set(sys.argv)): # sys.argv converted to set to remove the duplicate switches
        if not sw.startswith(('', '/', '-', '--')): continue # valid switches can start with `nothing` / - --
        func = option.option_method[sw] # func is __wrapper__ in __call__ that defined in Options class
        eval(f"{func}({i + 1})") # if switch has input, I should pass the location of input to func, if it hasn't, it will be handle in __wrapper__ with has_input

@exception_handler(KeyboardInterrupt, cause=f"Ctrl+C")
@exception_handler(JSONDecodeError, cause=f"<{PASSWD_FILE}> is corrupted!")
@exception_handler(FileNotFoundError, cause=f"<{PASSWD_FILE}> not found! if you have backup, restore it")
def main() -> None:
    pprint(BANNER)
    goodbye(
        len(sys.argv) == 1,
        cause='Not to use [bold]Switches[/bold]'
    )
    manage()

if __name__ == '__main__':
    main()
