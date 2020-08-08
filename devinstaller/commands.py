# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 16:55:05 IST
# Last-Updated: Sat  1 Aug 2020 21:20:16 IST
#
# commands.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles all the required logic to run shell commands
#
# Copyright (c) 2020, Justin Kizhakkinedath
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

"""Handles everything related to running shell commands"""
import re
import shlex
import subprocess

from devinstaller import exceptions as e
from devinstaller import models as m


def run_shell(command: str) -> None:
    """Runs the comand and returns None if no error else `subprocess.CalledProcessError` is raised

    Args:
        command: The path to the file

    Raises:
        CommandFailed
    """
    try:
        subprocess.run(shlex.split(command), capture_output=True, check=True)
    except subprocess.CalledProcessError as err:
        raise e.CommandFailed(returncode=err.returncode, cmd=err.cmd)


def run_python(python_code: str):
    pass


def launch_python(python_fun_name: str):
    pass


def run(command: str) -> None:
    """Run shell or python command
    """
    res = check_cmd(command)
    command_functions = {"py": run_python, "sh": run_shell}
    command_functions[res.prog](res.cmd)


def check_cmd(command: str) -> m.CommandResponse:
    """Check the command and returns the command response object
    """
    try:
        pattern = r"^(py|sh): (.*)"
        result = re.match(pattern, command)
        assert result is not None
        data = m.CommandResponse(prog=result.group(0), cmd=result.group(1))
        return data
    except AssertionError:
        raise e.SpecificationError(
            error=command,
            error_code="S100",
            message="The command didn't conform to the spec",
        )
