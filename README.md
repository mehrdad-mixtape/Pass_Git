# Pass_Git
Useful Script to Store &amp; Encrypt Your Classic-GitHub-Token On your Local System!

## Intro:
    - Store your Classic-Github-Token(passwd) in Encrypted format on your local system!
    - Decrypt your Classic-Github-Token(passwd) with your key
    - Encryption Algorithm is AES

## Helps:
```bash
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
    [bold][yellow]-b --backup[/yellow][/bold]: Make backup from [yellow]<{PASSWD_FILE}>.bkup[/yellow] on home directory
        $ passgit -b
    [bold][pink]-r --restore[/pink][/bold]: Restore your backup from [yellow]<{PASSWD_FILE}>.bkup[/yellow] to [yellow]<{PASSWD_FILE}>[/yellow]
        $ passgit -r
    [bold][medium_violet_red]-l --list[/medium_violet_red][/bold]: Show the list of available files in your home directory
        $ passgit -l
    [bold][dark_orange]-h --help[/dark_orange][/bold]: Show help
        $ passgit -h
    [bold][purple]passgit -g --give <1-{MAX_PASSWD}>[/purple][/bold]: Give you your decrypted passwd by index number between 1 and {MAX_PASSWD}
        $ passgit -g 1 // Give your the first stored passwd in [yellow]<{PASSWD_FILE}>[/yellow]
```