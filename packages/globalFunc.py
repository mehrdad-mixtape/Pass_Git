from .libs import (
    sys, inspect, os, hashlib, base64,
    log_console,
    List, Any,
    Random, AES,
)
from .logger import logger
from .decorators import exception_handler


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

pprint = lambda *args, **kwargs: log_console.print(*args, **kwargs)

def is_file_exist(file: str) -> bool:
    return file in os.listdir(f"{os.path.expanduser('~')}/")

def goodbye(expression: bool, cause: str='Unknown'):
    if expression:
        logger(f"{cause}", severity=1,
            nameno = inspect.getouterframes(inspect.currentframe())[1].filename.split('/')[-1],
            lineno = inspect.getouterframes(inspect.currentframe())[1].lineno
        )
        sys.exit()


def parse_range_test_cases(test_cases: str) -> List[int]:
    """ Parse and Sort range test-case 1-5,6,7-10 --> 1,2,3,4,5,6,7,8,9,10 """

    number_cases:List[int] = []

    for case in test_cases.split(','):
        goodbye(
            ',' not in case and case.count('-') > 1,
            cause=f"Invalid range format in {test_cases} detected!"
        )

        if '-' in case:
            s, e = map(int, case.split('-'))

            if s > e: e, s = s, e
            number_cases.extend(list(range(s, e + 1)))

        else: number_cases.append(int(case))
    
    return sorted(set(number_cases))


def press_any(who: str='WIZARD: ', msg: str='Continue', typ: str='s', clear: bool=False) -> Any:
    """
        Simple Interactive Function!

        @parmas:
            msg: message to show
            typ: type of Interaction:
            typ
                = 's' or 'S': simple mode just press any key!
                = 'yn' or 'YN: yes or no answer
                = 'q' of 'Q': question and answer
    """
    try:
        match typ:
            case 's' | 'S':
                print()
                log_console.input(f"{who}Press Any Key to \"{msg}\" OR Press Ctrl+C to Exit")
                print()

            case 'yn' | 'YN':
                while True:
                    print('\n' * 2)

                    pprint(f"{who}{msg}")
                    answer = log_console.input(f"{who}Y/N (default=Y): ")

                    if not answer or answer in ("y Y"): return True
                    elif answer not in ("y n Y N"): continue
                    else: return False

            case 'ny' | 'NT':
                while True:
                    print('\n' * 2)

                    pprint(f"{who}{msg}")
                    answer = log_console.input(f"{who}Y/N (default=N): ")

                    if not answer or answer in ("n N"): return True
                    elif answer not in ("y n Y N"): continue
                    else: return False

            case 'q' | 'Q':
                print('\n' * 2)

                while True:
                    temp_answer = log_console.input(f"{who}{msg} ")
                    if not temp_answer: continue

                    sure_answer = log_console.input(f"{who}Are you Sure? Y/N (default=Y): ")

                    if not sure_answer or sure_answer in ("y Y"): return temp_answer
                    elif sure_answer not in ("y n Y N") or sure_answer in ("n N"): continue

            case _: raise ValueError(f"Invalid {typ=}")

        if clear: print('\033c')

    except KeyboardInterrupt:
        sys.exit()
