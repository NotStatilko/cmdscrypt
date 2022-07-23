from setuptools import setup

setup(
    name = "cmdscrypt",
    version = '1.0',
    py_modules = ['cmdscrypt'],
    license = 'MIT',
    description = 'A simple app for generating urlsafe_b64 encoded scrypt keys',
    author_email = 'thenonproton@pm.me',
    url = 'https://github.com/NotStatilko/cmdscrypt',
    download_url = 'https://github.com/NotStatilko/cmdscrypt/archive/refs/tags/v1.0.tar.gz',
    entry_points = '''
        [console_scripts]
        cmdscrypt=cmdscrypt:app
    ''',
)
