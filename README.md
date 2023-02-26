# Pass_Git
Useful Script to Store &amp; Encrypt Your Classic-GitHub-Token On your Local System!

## Intro:
    - Store your Classic-Github-Token(passwd) in Encrypted format on your local system!
    - Decrypt your Classic-Github-Token(passwd) with your key
    - Encryption Algorithm is AES

## Helps:
```bash
    -n --new: Get your passwd and encrypt it, then will make new <.github_passwd.json> in your home directory
        $ passgit -n
    -a --add: Add new passwd on <.github_passwd.json>, passgit support maximum 20 passwd to encrypt and store
        $ passgit -a
    -d --dump: Dump all passwd <.github_passwd.json>
        $ passgit -d
    -b --backup: Make backup from <.github_passwd.json>.bkup on home directory
        $ passgit -b
    passgit <1-20>: Give you your decrypted passwd by index number between 1 and 20
        $ passgit 1 // Give your the first stored passwd in <.github_passwd.json>
```