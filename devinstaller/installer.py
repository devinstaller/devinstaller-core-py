# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Sat 18 Jul 2020 22:41:11 IST
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
from typing import Dict, List, Optional

from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m


def main(module_map: m.ModuleMapType, requirements_list: List[str]) -> None:
    """The entry point function

    Args:
        module_map: The module map of the current platform
        requirements_list: The list of modules to be installed
    """
    for module_name in requirements_list:
        traverse(module_map, module_name)


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
    if not module.installed:
        if module.requires is not None:
            for neighbour in module.requires:
                traverse(module_map, neighbour)
        else:
            execute(module_map, module_name)
            module.installed = True


def execute(
    module_map: m.ModuleMapType, module_name: str
) -> m.ModuleInstalledResponseType:
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
    if module_name in module_map:
        module = module_map[module_name]
        response = module_install_functions[module.module_type](module)
        return response
    raise e.SpecificationError(
        module_name, "S100", f"I was unable to find the module: {module_name}"
    )


def install_module(module: m.Module) -> m.ModuleInstalledResponseType:
    """The function which installs app modules

    Args:
        module: The app module

    Returns:
        The response object of the module
    """
    print("Installing module: {name}...".format(name=module.display))
    response: m.ModuleInstalledResponseType = {
        "init": install_steps(module.init),
        "command": install_command(module),
        "config": install_steps(module.config),
    }
    return response


def install_command(module: m.Module) -> Optional[m.CommandRunResponseType]:
    """The function which installs the module.

    Args:
        module: The app module

    Returns:
        The response object of the main install command
    """
    if module.command is None:
        print("skipping installation for {name}".format(name=module.display))
        return None
    return c.run(module.command)


def install_steps(
    steps: Optional[List[str]],
) -> Optional[List[m.CommandRunResponseType]]:
    """The function which handles installing of multi step commands.

    Args:
        steps: The list of steps which needs to be executed

    Returns:
        List of response object corresponding to each step
    """
    if steps is not None:
        response: List[m.CommandRunResponseType] = []
        for step in steps:
            response.append(c.run(step))
        return response
    return None


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


module_install_functions = {
    "app": install_module,
    "file": create_file,
    "folder": create_folder,
}
