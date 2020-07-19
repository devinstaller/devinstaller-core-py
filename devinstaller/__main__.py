# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:10:17 IST
# Last-Updated: Sat 18 Jul 2020 18:45:14 IST
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
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------

"""The main entrypoint module for running CLI commands
"""
import os
from typing import Optional

import click

from devinstaller import app as a
from devinstaller import exceptions as e

DEFAULT_DOC_FILE_PATH = os.getcwd() + "/sample.devfile.yml"


@click.group()
def main() -> None:
    """Main entrypoint function. Everything in this run before any of the
    subcommand
    """


@main.resultcallback()
def process_result() -> None:
    """Final callback function. Runs after the end of everything."""
    click.secho("Bye. Have a good day.", fg="green")


@main.command()
@click.option(
    "-f",
    "--file",
    "file_name",
    default=DEFAULT_DOC_FILE_PATH,
    help="Name of the install file. Default: `install.yaml`",
)
@click.option(
    "-p",
    "--platform",
    "platform",
    help=(
        "Name of the current platform. If not provided then I'll try to "
        "check if you have provided any help in the file."
        "For more information read the docs."
    ),
)
@click.option("--module", "module", help=("Name of the module you want to install. "))
def install(
    file_name: Optional[str], platform: Optional[str], module: Optional[str]
) -> None:
    """Install the default group and the modules which it requires
    """
    try:
        a.install(file_path=file_name, platform_codename=platform, module=module)
    except e.DevinstallerError as err:
        click.secho(str(err), fg="red")
    except e.SpecificationError as err:
        click.secho(str(err), fg="red")


@main.command()
@click.option(
    "-f",
    "--file",
    "file_name",
    default=DEFAULT_DOC_FILE_PATH,
    help="Name of the install file. Default: `install.yaml`",
)
def show(file_name: Optional[str]) -> None:
    """Show all the groups and modules available for your OS
    """
    try:
        assert file_name is not None
        a.show(file_name)
    except e.DevinstallerError as err:
        click.secho(str(err), fg="red")


# @main.command()
# @click.argument("commands", nargs=-1)
# def run(commands):
#     """where COMMANDS is your regular bash command

#     Example: Here `dev run brew install pipenv clang emacs` will install all
#     the packages using brew and add it into the spec automagically.
#     """
#     pass


if __name__ == "__main__":
    main()
