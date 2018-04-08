#!/usr/bin/env python3

from setuptools import setup

setup(
    name='vhost',
    version='0.1.0',
    description='Tool for help creating virtual hosts',
    author='Felipe Lopes',
    author_email='bolzin@gmail.com',
    url='https://www.github.com/felipebool/vhost',
    download_url='https://www.github.com/felipebool/vhost/archive/0.1.0.tar.gz',
    packages=['vhost'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'vhost = vhost.__main__:main'
        ]
    }
)

