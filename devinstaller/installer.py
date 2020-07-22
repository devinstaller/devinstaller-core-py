# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Wed 22 Jul 2020 18:31:12 IST
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
import sys
from typing import Callable, Dict, List, Set, Union

import questionary
from typeguard import typechecked

from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m
from devinstaller import utilities as u


@typechecked
def main(module_map: m.ModuleMapType, requirements_list: List[str]) -> None:
    """The entry point function

    Args:
        module_map: The module map of the current platform
        requirements_list: The list of modules to be installed
    """
    orphan_list: Set[str] = set()
    for module_name in requirements_list:
        orphan_list = traverse(module_map, module_name, orphan_list)
    if orphan_list != set():
        if ask_user_for_uninstalling_orphan_modules(orphan_list):
            uninstall_modules(orphan_list, module_map)


@typechecked
def uninstall_modules(orphan_list: Set[str], module_map: m.ModuleMapType) -> None:
    """The main function for uninstalling modules.

    This function is used to uninstall orphan modules.

    Args:
        orphan_list: The "list" of modules which are not used by any other modules
        module_map: The module map for the current platform
    """
    module_uninstall_functions: Dict[str, Callable[[m.Module], None]] = {
        "app": uninstall_app_module,
        "file": uninstall_file_module,
        "folder": uninstall_folder_module,
        "link": uninstall_link_module,
        "phony": uninstall_phony_module,
    }
    for module_name in orphan_list:
        module = module_map[module_name]
        module_uninstall_functions[module.module_type](module)
    return None


@typechecked
def ask_user_for_uninstalling_orphan_modules(orphan_list: Set[str]) -> bool:
    """Asks user for confirmation for the uninstallation of the orphan modules.

    Args:
        orphan_list: The "list" of modules which are not used by any other modules
    """
    print(
        "Because of failed installation of some modules, there are some"
        "modules which are installed but not required by any other modules"
    )
    orphan_module_names = ", ".join(name for name in orphan_list)
    print(f"These are the modules: {orphan_module_names}")
    response = u.ask_user_confirmation("Do you want to uninstall?")
    return response


@typechecked
def traverse(
    module_map: m.ModuleMapType, module_name: str, orphan_list: Set[str]
) -> Set[str]:
    """Reverse DFS logic for traversing dependencies.

    Basically it installs all the dependencies first then app.

    Args:
        module_map: The module map of current platform
        module_name: The name of the module to traverse
        orphan_list: The list of modules which are not used by any other modules

    Raises:
        SpecificationError
            if one of your module requires but the required module itself is not present
    """
    try:
        module = module_map[module_name]
    except KeyError:
        raise e.SpecificationError(
            error=module_name,
            error_code="S100",
            message="The name of the module given by you didn't match with the codenames of the modules",
        )
    if module.status is not None:
        if module.alias in orphan_list:
            orphan_list.remove(module.alias)
        return orphan_list
    module.status = "in progress"
    orphan_list = traverse_requires(
        module_map=module_map, module=module, orphan_list=orphan_list
    )
    orphan_list = traverse_optionals(
        module_map=module_map, module=module, orphan_list=orphan_list
    )
    orphan_list = traverse_install(module, orphan_list)
    return orphan_list


@typechecked
def traverse_requires(
    module_map: m.ModuleMapType, module: m.Module, orphan_list: Set[str]
) -> Set[str]:
    if module.requires is not None:
        for index, child in enumerate(module.requires):
            orphan_list = traverse(module_map, child, orphan_list)
            if module_map[child].status == "failed":
                print(
                    f"The module {child} in the requires of {module.alias} has failed"
                )
                module.status = "failed"
                orphan_list.update(module.requires[:index])
                return orphan_list
    return orphan_list


@typechecked
def traverse_optionals(
    module_map: m.ModuleMapType, module: m.Module, orphan_list: Set[str]
) -> Set[str]:
    if module.optionals is not None:
        for child in module.optionals:
            orphan_list = traverse(module_map, child, orphan_list)
            if module_map[child].status == "failed":
                print(
                    f"The module {child} in the optionals of {module.alias} has failed, but the installation for remaining modules will continue"
                )
    return orphan_list


@typechecked
def traverse_install(module: m.Module, orphan_list: Set[str]) -> Set[str]:
    try:
        install_module(module)
        module.status = "success"
        return orphan_list
    except e.ModuleInstallationFailed:
        print(
            f"The installation for the module: {module.alias} failed. And all the instructions has been rolled back."
        )
        module.status = "failed"
        if module.requires is not None:
            orphan_list.update(module.requires)
        if module.optionals is not None:
            orphan_list.update(module.optionals)
        return orphan_list


@typechecked
def install_module(module: m.Module) -> None:
    """Common entry point for installing any module.

    Args:
        module: The module you want to install

    Returns:
        None if all good

    Raises:
        SpecificationError
            with error code :ref:`error-code-S100`
    """
    module_install_functions: Dict[str, Callable[[m.Module], None]] = {
        "app": install_app_module,
        "file": install_file_module,
        "folder": install_folder_module,
        "link": install_link_module,
        "group": install_group_module,
        "phony": install_phony_module,
    }
    try:
        module_install_functions[module.module_type](module)
        return None
    except KeyError:
        raise e.SpecificationError(
            module.module_type,
            "S100",
            f"The module_type: {module.module_type} is invalid.",
        )


@typechecked
def append_if_not_none(
    *data: Union[m.ModuleInstallInstruction, List[m.ModuleInstallInstruction], None]
) -> List[m.ModuleInstallInstruction]:
    """Returns a list with all the data combined.

    This is used to combine the `init`, `command` and `config` instructions so
    that they can be run in a single function.

    Args:
        Any number of arguments. The arguments are expected to be of either
        ModuleInstallInstruction or list of ModuleInstallInstruction
    """
    temp_list = []
    for i in data:
        if i is not None:
            if isinstance(i, list):
                temp_list += i
            else:
                temp_list.append(i)
    return temp_list


@typechecked
def rollback_instructions(instructions: List[m.ModuleInstallInstruction]) -> None:
    """Rollback the installation of a module

    Args:
        List of install instructions

    Raises:
        ModuleRollbackFailed
            if the rollback instructions fails
    """
    for step in instructions:
        if step.rollback is not None:
            try:
                print(f"Rolling back `{step.install}` using `{step.rollback}`")
                c.run(step.rollback)
            except e.CommandFailed:
                raise e.ModuleRollbackFailed
    return None


@typechecked
def install_steps(steps: List[m.ModuleInstallInstruction]) -> None:
    """The function which handles installing of multi step commands.

    Args:
        steps: The list of steps which needs to be executed

    Raises:
        ModuleInstallationFailed
            if the installation of the module fails
        ModuleRollbackFailed
            if the rollback command fails
    """
    if steps == []:
        return None
    for index, step in enumerate(steps):
        try:
            c.run(step.install)
        except e.CommandFailed:
            revert_list = steps[:index]
            revert_list.reverse()
            try:
                rollback_instructions(revert_list)
            except e.ModuleRollbackFailed:
                raise e.ModuleRollbackFailed
            raise e.ModuleInstallationFailed
    return None


def uninstall_app_module(module: m.Module) -> None:
    """Uninstall the module using its rollback instructions.

    Args:
        module: The module which you want to uninstall
    """
    print(f"Uninstalling module: {module.display}...")
    installation_steps = append_if_not_none(module.init, module.command, module.config)
    try:
        rollback_instructions(installation_steps)
    except e.ModuleRollbackFailed:
        print(f"Rollback instructions for {module.display} failed. Crashing program.")
        sys.exit(1)
    return None


def uninstall_file_module(module: m.Module) -> None:
    pass


def uninstall_folder_module(module: m.Module) -> None:
    pass


def uninstall_link_module(module: m.Module) -> None:
    pass


def uninstall_phony_module(module: m.Module) -> None:
    pass


@typechecked
def install_app_module(module: m.Module) -> None:
    """The function which installs app modules

    Args:
        module: The app module

    Returns:
        The response object of the module
    """
    print(f"Installing module: {module.display}...")
    installation_steps = append_if_not_none(module.init, module.command, module.config)
    try:
        install_steps(installation_steps)
    except e.ModuleRollbackFailed:
        print(f"Rollback instructions for {module.display} failed. Crashing program.")
        sys.exit(1)
    return None


@typechecked
def install_file_module(module: m.Module) -> str:
    """The function which will create the required file

    Args:
        module: The file module
    """
    print("Creating file: {name}...".format(name=module.display))
    raise NotImplementedError


@typechecked
def install_folder_module(module: m.Module) -> None:
    """The function which will create the required folder

    Args:
        module: The folder module
    """
    print("Creating folder: {name}...".format(name=module.display))
    raise NotImplementedError


def install_link_module(module: m.Module) -> None:
    pass


def install_group_module(module: m.Module) -> None:
    pass


def install_phony_module(module: m.Module) -> None:
    pass
