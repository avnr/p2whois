from setuptools import setup

setup(
    name = 'p2whois',
    packages = ['p2whois'],
    version = '0.5',
    description = 'Proxy to Prefix WhoIs',
    author = 'Avner Herskovits',
    author_email = 'avnr_ at outlook.com',
    url = 'https://github.com/avnr/p2whois',
    download_url = 'https://github.com/avnr/p2whois/tarball/0.4',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
