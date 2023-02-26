#!/bin/python3.10

import os, sys, base64, hashlib, getpass
from typing import List
from subprocess import run
try:
    from pyperclip import copy
    method = 'active'
except ImportError:
    method = 'native'

try:
    from Crypto import Random
    from Crypto.Cipher import AES
except ImportError as E:
    sys.exit(f"{E}\nPlease install 'pycryptodome' pkg, pip3 install pycryptodome")

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
        except UnicodeDecodeError as E:
            sys.exit(f"{E}")

    def __pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s)-1:])]

def main(argv: List[str]) -> None:
    passwd_path = f"{os.path.expanduser('~')}/.github_passwd"
    if len(argv) != 2:
        try:
            with open(passwd_path, mode='r') as file:
                passwd = file.readline().strip('\n').strip(' ').encode('utf-8')
                aes = AESCipher(getpass.getpass('Give me your key: '))
                try:
                    clear_passwd = aes.decrypt(passwd)
                    copy(clear_passwd) if method == 'active' else run(f"echo {clear_passwd} | xsel --clipboard --input")
                    print('Password copied to clipboard!')
                    del passwd
                except Exception:
                    print(f"Please install 'pyperclip' pkg (pip3 install pyperclip) or xsel to save passwd on clipboard")
        except FileNotFoundError as E:
            sys.exit(f"{E}\nPlease run command with -n or --new")
    else:
        if argv[1] in '-n --new':
            aes = AESCipher(getpass.getpass('Give me your key: '))
            clear_passwd = getpass.getpass('Give me your new Github passwd: ')
            with open(passwd_path, mode='w') as file:
                cipher_passwd = aes.encrypt(clear_passwd)
                file.write(cipher_passwd.decode('utf-8'))
                print(f"Passwd stored on '{passwd_path}'")
        else:
            sys.exit("Help:\noptions:\n\t-n or --new")

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        sys.exit()
