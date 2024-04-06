#!/usr/bin/env python3
"""
This is a simple script that generates
passwords from given master-phrase &
salt [unique text], based on Scrypt.
"""
import click

from base64 import urlsafe_b64encode
from hashlib import scrypt
from traceback import format_exception


def init_terminal():
    if click.utils.should_strip_ansi():
        clear_terminal()
    else:
        print('\n'*80)

def clear_terminal(exitp: bool=False):
    if click.utils.should_strip_ansi():
        click.termui.clear()
        print('\n'*100)
    else:
        if exitp:
            for _ in range(80):
                print('\033[2K', end='') # Erase one line
                print('\033[F', end='') # Move cursor 1 line UP
        else:
            for _ in range(10):
                print('\033[2K', end='') # Erase one line
                print('\033[F', end='') # Move cursor 1 line UP

            print('\n'*8, end='')


@click.group()
def cli_group():
    pass

@cli_group.command()
@click.option(
    '--password', '-p', prompt=True, hide_input=True,
    help='Your password/passphrase'
)
@click.option(
    '--password-hex', is_flag=True,
    help='Decode --pass as hexadecimal to bytes'
)
@click.option(
    '--scrypt-salt', '-S', 'salt', prompt=True,
    help='Scrypt Salt as hexadecimal'
)
@click.option(
    '--salt-hex', is_flag=True,
    help='Decode --scrypt-salt as hexadecimal to bytes'
)
@click.option(
    '--scrypt-n', '-N', 'n',
    help='Scrypt N', default=2**20,
)
@click.option(
    '--scrypt-p', '-P', 'p',
    help='Scrypt P', default=1,
)
@click.option(
    '--scrypt-r', '-R', 'r',
    help='Scrypt R', default=8,
)
@click.option(
    '--scrypt-dklen', '-L', 'l',
    help='Scrypt key Length', default=32
)
@click.option(
    '--maxmem', '-M', 'm',
    help='Scrypt maxmem'
)
@click.option(
    '--out-base64', is_flag=True,
    help='Output resulted key as Urlsafe base64',
)
@click.option(
    '--out-hex', is_flag=True,
    help='Output resulted key as Hex instead of raw bytes',
)
@click.option(
    '--outfile', type=click.Path(writable=True),
    help='Write resulted key to specified file',
)
def cli(password, password_hex, salt, salt_hex, n, p, r, l, m, out_base64, out_hex, outfile):
    """Use CMDScrypt in CLI mode (see --help)"""

    m = m if m else (128 * r * (n + p + 2))

    if salt_hex:
        salt = bytes.fromhex(salt)
    else:
        salt = salt.encode()

    if password_hex:
        password = bytes.fromhex(password)
    else:
        password = password.encode()

    key = scrypt(password, salt=salt,
        n=n, r=r, p=p, dklen=l, maxmem=m)

    if out_hex:
        key = key.hex()

    elif out_base64:
        key = urlsafe_b64encode(key)

    if outfile:
        key = key if isinstance(key, bytes) else key.encode()

        with open(outfile, 'wb') as f:
            f.write(key)
    else:
        click.echo(key, nl=False)


@cli_group.command()
@click.option(
    '--password-hex', is_flag=True,
    help='Decode --pass as hexadecimal to bytes'
)
@click.option(
    '--salt-hex', is_flag=True,
    help='Decode --scrypt-salt as hexadecimal to bytes'
)
@click.option(
    '--scrypt-n', '-N', 'n',
    help='Scrypt N', default=2**20,
)
@click.option(
    '--scrypt-p', '-P', 'p',
    help='Scrypt P', default=1,
)
@click.option(
    '--scrypt-r', '-R', 'r',
    help='Scrypt R', default=8,
)
@click.option(
    '--scrypt-dklen', '-L', 'l',
    help='Scrypt key Length', default=32
)
@click.option(
    '--maxmem', '-M', 'm',
    help='Scrypt maxmem'
)
@click.option(
    '--out-hex', is_flag=True,
    help='Output resulted key as Hex instead of Base64',
)
@click.option(
    '--out-raw', is_flag=True,
    help='Output resulted key as raw bytestring',
)
@click.option(
    '--outfile', type=click.Path(writable=True),
    help='Write resulted key to specified file',
)
def tui(password_hex, salt_hex, n, p, r, l, m, out_hex, out_raw, outfile):
    """Use CMDScrypt in TUI mode (see --help)"""

    if out_raw and not outfile:
        click.secho('--out-raw can be used only with --outfile', fg='red')
        return

    init_terminal()

    m = m if m else (128 * r * (n + p + 2))

    print('! WARNING: All written text will be VISIBLE!')
    print(f'! WARNING: We will use {round(m/1024**3,1)}GB of RAM!')

    try:
        password = input('\n> Passphrase: ')

        if password_hex:
            password = bytes.fromhex(password)
        else:
            password = password.encode()

        while True:
            clear_terminal()

            salt = input('>> Salt [unique text]: ')

            if salt_hex:
                salt = bytes.fromhex(salt)
            else:
                salt = salt.encode()

            clear_terminal()
            print('@ In process. Please wait...')

            key = scrypt(password, salt=salt,
                n=n, r=r, p=p, dklen=l, maxmem=m)

            clear_terminal()

            if out_hex:
                key = key.hex()
            else:
                key = urlsafe_b64encode(key).decode()

            if outfile:
                key = key if isinstance(key, bytes) else key.encode()

                with open(outfile, 'wb') as f:
                    f.write(key)

                print(
                    f'''RESULTED PASSWORD WAS WRITTEN TO FILE\n\n'''

                     '''% Press Enter to make another & re-write, Ctrl+C to exit.'''
                )
                input()
            else:
                print(
                    f'''RESULTED PASSWORD:\n  {key}\n\n'''

                     '''% Press Enter to make another, Ctrl+C to exit.'''
                )
                input()

    except KeyboardInterrupt:
        clear_terminal(exitp=True)


def safe_cmdscrypt_startup():
    try:
        cli_group()
    except Exception as e:
        traceback = ''.join(format_exception(
            e,
            value = e,
            tb = e.__traceback__
        ))
        click.secho(traceback, fg='red'); exit(1)

if __name__ == '__main__':
    safe_cmdscrypt_startup()
