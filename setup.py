import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='link_getter',
    version='0.1',
    packages=['link_getter'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Use this package, get links and have fun!',
    long_description=README,
    url='https://github.com/MarlyasDad/link_getter',
    author='Alex Yudaev',
    author_email='yudaev.alex@gmail.com',
    keywords=['html', 'link', 'requests'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'linkget = link_getter.main:main',
        ]
    },
)
