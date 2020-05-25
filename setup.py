from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='devin',
    version='0.1.0',
    description=('Scaffold tool for developers'),
    long_description=long_description,
    author='Bruce Wayne',
    author_email='bruce.wayne@example.com',
    url='https://github.com/bast/somepackage',
    license='MIT',
    packages=['devin'],
#   no dependencies in this example
#   install_requires=[
#       'dependency==1.2.3',
#   ],
#   no scripts in this example
#   scripts=['bin/a-script'],
    entry_points={
        'console_scripts': ['dev=devin.__main__:main'],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6'],
    )
