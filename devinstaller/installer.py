# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Fri 17 Jul 2020 18:46:24 IST
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


def main(graph: Dict[str, m.Module], requirements_list: List[str]) -> None:
    """The entry point function

    Args:
        graph: The dependency list(graph) showing all the modules which has dependencies
        requirements_list: The list of modules to be installed
    """
    for module_name in requirements_list:
        traverse(graph, module_name)


def traverse(graph: Dict[str, m.Module], module_name: str) -> None:
    """Reverse DFS logic for traversing dependencies.
    Basically it installs all the dependencies first then app.

    Args:
        graph: The dependency list(graph) showing all the modules which has dependencies
        module_name: The name of the module to traverse
    """
    module = graph[module_name]
    if not module.installed:
        if module.requires is not None:
            for neighbour in module.requires:
                traverse(graph, neighbour)
        else:
            execute(graph, module_name)
            module.installed = True


def execute(
    graph: Dict[str, m.Module], module_name: str
) -> Optional[m.ModuleInstalledResponseType]:
    """Common entry point for installing all the modules.

    Args:
        graph: The dependency list(graph) showing all the modules which has dependencies
        module_name: The name of the module to traverse

    Returns:
        The response object containing the status of all the commands

    Raises:
        RuleViolationError
            with error code :ref:`error-code-104`
    """
    if module_name in graph:
        module = graph[module_name]
        return function[module.module_type](module)
    raise e.RuleViolationError(
        rule_code=104, message=f"I was unable to find the module: {module_name}"
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


function = {"app": install_module, "file": create_file, "folder": create_folder}
