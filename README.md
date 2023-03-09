# Pass_Git
Useful Script to Store &amp; Encrypt Your Classic-GitHub-Token On your Local System!

## Intro:
    - Store your Classic-Github-Token(passwd) in Encrypted format on your local system!
    - Decrypt your Classic-Github-Token(passwd) with your key
    - Encryption Algorithm is AES

## Interview:
![image](https://github.com/mehrdad-mixtape/Pass_Git/blob/master/images/index.png)

## Helps:
```bash
Helps:
    -n --new: Get your passwd and encrypt it, then will make new <.github_passwd.json> in your home directory
        $ passgit -n
    -a --add: Add new passwd on <.github_passwd.json>, passgit support maximum 20 passwd to encrypt and store
        $ passgit -a
    -d --dump: Dump all passwd from <.github_passwd.json>
        $ passgit -d
    -b --backup: Make backup from <.github_passwd.json>.bkup on home directory
        $ passgit -b
    -r --restore: Restore your backup from <.github_passwd.json>.bkup to <.github_passwd.json>
        $ passgit -r
    -l --list: Show the list of available files in your home directory
        $ passgit -l
    -h --help: Show help
        $ passgit -h
    passgit -g --give <1-20>: Give you your decrypted passwd by index number between 1 and 20
        $ passgit -g 1 // Give your the first stored passwd in <.github_passwd.json>
```
