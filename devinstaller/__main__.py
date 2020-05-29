# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:10:17 IST
# Last-Updated: Fri 29 May 2020 16:46:17 IST
#
# __main__.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Main entrypoint
#
# Copyright (c) 2020, Justine Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "software"), to deal
#   in the software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the software, and to permit persons to whom the software is
#   furnished to do so, subject to the following conditions:
#
#   the above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the software.
#
#   the software is provided "as is", without warranty of any kind,
#   express or implied, including but not limited to the warranties of
#   merchantability, fitness for a particular purpose and noninfringement.
#   in no event shall the authors or copyright holders be liable for any claim,
#   damages or other liability, whether in an action of contract, tort or
#   otherwise, arising from, out of or in connection with the software or the use
#   or other dealings in the software.
# -----------------------------------------------------------------------------

from . import schema as s
from . import yaml as y
from . import commands as c

import click

@click.group()
def main():
    pass

SCHEMA_FILE_PATH = "assets/schema.yaml"
DEFAULT_DOC_FILE_PATH = "assets/sample.yml"

@main.command(help="Install the default preset and the modules which it requires.")
@click.option('-f', "--file", "file_name", default=DEFAULT_DOC_FILE_PATH, help="Name of the install file. Default: `install.yaml`")
@click.option('-p', '--preset', 'preset', help="Name of the preset you want to install. If not provided then the default preset will be installed.")
@click.option('-m', '--module', 'module', help="Name of the module you want to install. For more information on modules refer the docs.")
def install(file_name, preset, module):
    response = _validate_spec(file_name)
    if response:
        dependency = s.generate_dependency(document)
        print(dependency)


@main.command(help="List out all the presets and modules available for your OS.")
@click.option('-f', "--file", "file_name", default=DEFAULT_DOC_FILE_PATH, help="Name of the install file. Default: `install.yaml`")
@click.option('--platform', 'platform', help="Name of the platform for which you want to list out the names of presets and modules")
@click.option('-p', '--preset', 'preset', help="Name of the preset for which you want to list out the names of modules which will be installed")
def list(file_name, preset, platform):
    response = _validate_spec(file_name)
    if response:
        dependency = s.generate_dependency(document)
        print(dependency)


def _validate_spec(doc_file_path, schema_file_path=SCHEMA_FILE_PATH):
    schema = y.read(schema_file_path)
    document = y.read(doc_file_path)
    response = s.validate(document, schema)
    if response["is_valid"]:
        return True
    else:
        print("You have errors in your yaml file")
        print(response["errors"])
        return False
