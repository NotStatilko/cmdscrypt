from setuptools import setup

setup(
    name             = 'cmdscrypt',
    version          =  '2.0',
    py_modules       =  ['cmdscrypt'],
    license          =  'MIT',
    description      =  'A simple CLI app for generating Scrypt keys',
    long_description = open('README.md', encoding='utf-8').read(),
    author_email     =  'thenonproton@pm.me',
    url              =  'https://github.com/NotStatilko/cmdscrypt',
    download_url     =  'https://github.com/NotStatilko/cmdscrypt/archive/refs/tags/v2.0.tar.gz',

    install_requires = ['click==8.1.3'],
    long_description_content_type='text/markdown',

    entry_points = '''
        [console_scripts]
        cmdscrypt=cmdscrypt:safe_cmdscrypt_startup
    ''',
)
