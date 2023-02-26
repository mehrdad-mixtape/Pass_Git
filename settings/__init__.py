INFO = '[green]Info[/green]'
DEBUG = '[purple]Debug[/purple]'
WARNING = '[dark_orange]Warning[/dark_orange]'
ERROR = '[red]Error[/red]'

PROJECT_NAME = '[blink][dark_orange]Passgit[/dark_orange][/blink]'

PASSWD_FILE = ".github_passwd.json"

MAX_PASSWD = 20

ALGO = '[purple]A[/purple][cyan]E[/cyan][yellow]S[/yellow]'

CGT = '[dark_orange]Classic-Github-Token(passwd)[/dark_orange]'

OPTIONS = f"""
Intro:
    Store your {CGT} in [blue]Encrypted[/blue] format on your local system!
    [green]Decrypt[/green] your {CGT} with your [red]key[/red]
    Encryption Algorithm is {ALGO}

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
