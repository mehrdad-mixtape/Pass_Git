INFO = '[green]Info[/green]'
NOTICE = '[purple]Notice[/purple]'
WARNING = '[dark_orange]Warning[/dark_orange]'
ERROR = '[red]Error[/red]'

PROJECT_NAME = '[blink][dark_orange]Passgit[/dark_orange][/blink]'

PASSWD_FILE = ".github_passwd.json"
PASSWD_FILE_BKUP = f"{PASSWD_FILE}.bkup"

MAX_PASSWD = 20

ALGO = '[purple]A[/purple][cyan]E[/cyan][yellow]S[/yellow]'

CGT = '[dark_orange]Classic-Github-Token(passwd)[/dark_orange]'

HELP = f"""
Intro:
    Store your {CGT} in [blue]Encrypted[/blue] format on your local system!
    [green]Decrypt[/green] your {CGT} with your [red]key[/red]
    Encryption Algorithm is {ALGO}

Helps:
    [bold][red]-n --new[/red][/bold]: Enter your passwd and encrypt it, then will make new [yellow]<{PASSWD_FILE}>[/yellow] in your home directory
        $ passgit -n
    [bold][green]-a --add[/green][/bold]: Add new passwd on [yellow]<{PASSWD_FILE}>[/yellow], passgit support maximum {MAX_PASSWD} passwd to encrypt and store
        $ passgit -a
    [bold][cyan]-d --dump[/cyan][/bold]: Dump all passwd [yellow]<{PASSWD_FILE}>[/yellow]
        $ passgit -d
    [bold][yellow]-b --backup[/yellow][/bold]: Make backup from [yellow]<{PASSWD_FILE}>.bkup[/yellow] on home directory
        $ passgit -b
    [bold][pink]-r --restore[/pink][/bold]: Restore your backup from [yellow]<{PASSWD_FILE}>.bkup[/yellow] to [yellow]<{PASSWD_FILE}>[/yellow]
        $ passgit -r
    [bold][medium_violet_red]-l --list[/medium_violet_red][/bold]: Show the list of available files in your home directory
        $ passgit -l
    [bold][dark_orange]-h --help[/dark_orange][/bold]: Show help
        $ passgit -h
    [bold][purple]-g --give[/purple][/bold]: Enter your decrypted passwd by index number between 1 and {MAX_PASSWD}
        $ passgit -g <1-{MAX_PASSWD}> // Enter your passwd number
"""
