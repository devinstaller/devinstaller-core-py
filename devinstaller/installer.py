# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Tue 21 Jul 2020 17:57:10 IST
#
# installer.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Everything related to installer
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

"""Handles the main how to install the modules logic"""
import subprocess
import sys
from typing import List, Union

from typeguard import typechecked

from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m


@typechecked
def main(module_map: m.ModuleMapType, requirements_list: List[str]) -> None:
    """The entry point function

    Args:
        module_map: The module map of the current platform
        requirements_list: The list of modules to be installed
    """
    for module_name in requirements_list:
        traverse(module_map, module_name)


@typechecked
def traverse(module_map: m.ModuleMapType, module_name: str) -> None:
    """Reverse DFS logic for traversing dependencies.
    Basically it installs all the dependencies first then app.

    Args:
        module_map: The module map of current platform
        module_name: The name of the module to traverse
    """
    try:
        module = module_map[module_name]
    except KeyError:
        raise e.SpecificationError(
            error=module_name,
            error_code="S100",
            message="The name of the module given by you didn't match with the codenames of the modules",
        )
    if module.status is None:
        module.status = "in progress"
        if module.requires is not None:
            for neighbour in module.requires and module.status != "failed":
                traverse(module_map, neighbour)
                if module_map[neighbour].status == "failed":
                    print(
                        f"The module {neighbour} in the requires of {module.alias} has failed"
                    )
                    module.status = "failed"
        if module.optionals is not None:
            for neighbour in module.optionals and module.status != "failed":
                traverse(module_map, neighbour)
                if module_map[neighbour].status == "failed":
                    print(
                        f"The module {neighbour} in the optionals of {module.alias} has failed, but the installation will continue"
                    )
        else:
            module.status = execute(module_map, module_name)


def execute(module_map: m.ModuleMapType, module_name: str) -> str:
    """Common entry point for installing all the modules.

    Args:
        module_map: The module map of current platform
        module_name: The name of the module to traverse

    Returns:
        The response object containing the status of all the commands

    Raises:
        SpecificationError
            with error code :ref:`error-code-S100`
    """
    module_install_functions = {
        "app": install_module,
        "file": create_file,
        "folder": create_folder,
    }
    if module_name in module_map:
        module = module_map[module_name]
        response = module_install_functions[module.module_type](module)
        return response
    raise e.SpecificationError(
        module_name, "S100", f"I was unable to find the module: {module_name}"
    )


def install_module(module: m.Module) -> str:
    """The function which installs app modules

    Args:
        module: The app module

    Returns:
        The response object of the module
    """
    print("Installing module: {name}...".format(name=module.display))
    installation_steps = append_if_not_none(module.init, module.command, module.config)
    try:
        install_steps(installation_steps)
    except subprocess.CalledProcessError:
        print("Rolling back commands")


@typechecked
def append_if_not_none(
    *data: Union[m.ModuleInstallInstruction, List[m.ModuleInstallInstruction], None]
) -> List[m.ModuleInstallInstruction]:
    """Returns a list with all the data combined.

    This is used to combine the `init`, `command` and `config` instructions so that they can be run in a single function.

    Args:
        Any number of arguments. The arguments are expected to be of either ModuleInstallInstruction
        or list of ModuleInstallInstruction
    """
    temp_list = []
    for i in data:
        if i is not None:
            if isinstance(i, list):
                temp_list += i
            else:
                temp_list.append(i)
    return temp_list


def rollback_instructions(instructions: List[m.ModuleInstallInstruction]) -> None:
    """Rollbacks instructions used for the installation of a module

    Args:
        List of install instructions

    Raises:
        InstallerRollbackFailed if the rollback instructions fails
    """
    for index, step in enumerate(instructions):
        if step.revert is not None:
            try:
                print(f"Rolling back `{step.install}` using `{step.rollback}`")
                c.run(step.rolback)
            except subprocess.CalledProcessError:
                raise e.InstallerRollbackFailed


@typechecked
def install_steps(steps: List[m.ModuleInstallInstruction]) -> None:
    """The function which handles installing of multi step commands.

    Args:
        steps: The list of steps which needs to be executed

    Raises:
        subprocess.CalledProcessError if the command fails
    """
    for index, step in enumerate(steps):
        try:
            c.run(step.install)
        except subprocess.CalledProcessError:
            revert_list = steps[:index]
            revert_list.reverse()
            try:
                rollback_instructions(revert_list)
            except e.InstallerRollbackFailed:
                print("Rollback instructions also failed. Crashing program.")
                sys.exit(1)
            raise e.InstallerModuleFailed("Instructions failed. Rolling back")


def create_file(module: m.Module):
    """The function which will create the required file

    Args:
        module: The file module
    """
    print("Creating file: {name}...".format(name=module.display))
    raise NotImplementedError


def create_folder(module: m.Module):
    """The function which will create the required folder

    Args:
        module: The folder module
    """
    print("Creating folder: {name}...".format(name=module.display))
    raise NotImplementedError
