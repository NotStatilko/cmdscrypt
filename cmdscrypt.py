#!/usr/bin/env python3
"""
This is a simple script that generates
passwords from given master-phrase &
salt [unique text], based on Scrypt.
"""
from base64 import urlsafe_b64encode
from hashlib import scrypt

from sys import platform, argv
from os import system

if platform.startswith('win'):
    clear_command = 'cls'
elif platform.startswith('cygwin'):
    clear_command = 'printf "\033c"'
else:
    clear_command = "printf '\33c\e[3J' || clear || cls"

def clear_terminal():
    system(clear_command)
    print('\n'*100)

clear_terminal()

if argv[1:]:
    configuration = [int(i) for i in argv[1:]]
else:
    configuration = [2**20, 8, 1, 32]

n, r, p, dklen = configuration 
maxmem = (128 * r * (n + p + 2))

print('! WARNING: All written text will be VISIBLE!')
print(f'! WARNING: We will use {round(maxmem/1024**3,1)}GB of RAM!')

def app():
    try:
        password = input('\n> Passphrase: ').encode()

        while True:
            clear_terminal()

            salt = input('>> Salt [unique text]: ').encode()

            clear_terminal()
            print('@ In process. Please wait...')

            key = scrypt(
                password, 
                salt=salt,
                n=n, r=r, p=p, 
                dklen=dklen, 
                maxmem=maxmem
            )
            clear_terminal()
            print(
                f'''RESULTED PASSWORD:\n  {urlsafe_b64encode(key).decode()}\n\n'''

                 '''% Press Enter to make another, Ctrl+C to exit.'''
            )
            input()

    except KeyboardInterrupt:
        clear_terminal()

if __name__ == '__main__':
    app()
