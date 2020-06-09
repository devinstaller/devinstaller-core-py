# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Wed 10 Jun 2020 01:57:23 IST
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

from devinstaller import exceptions as e
from devinstaller import commands as c
from devinstaller import helpers as h


def main(graph, requirements_list):
    """The entry point function
    :param dict graph: The dependency list(graph) showing all the modules which
    has dependencies
    :param list requirements_list: The list of all the main modules to be
    installed
    :return: None
    :rtype: None
    """
    for module_name in requirements_list["requires"]:
        _traverse(graph, module_name)


def _traverse(graph, module_name):
    if not graph[module_name]["installed"]:
        if h.check_key("requires", graph[module_name]):
            for neighbour in graph[module_name]["requires"]:
                _traverse(graph, neighbour)
        else:
            _execute(module_name, graph)
            graph[module_name]["installed"] = True


def _execute(module_name, graph):
    if h.check_key(module_name, graph):
        module = graph[module_name]
        return function[module["type"]](module)
    print(f"I was unable to find the module: {module_name}")
    raise e.RuleViolation(rule_code=104)


def _install_module(module):
    print(f"Installing module: {module['name']}...")
    response = {}
    response["init"] = _install_steps(module, "init")
    response["command"] = _install_command(module)
    response["config"] = _install_steps(module, "config")
    return response


def _install_command(module):
    try:
        if module["command"] is None:
            print(f"skipping installation for {module['name']}")
            return None
        return c.run(module["command"])
    except KeyError:
        try:
            command = module["installer"].format(name=module["name"])
            return c.run(command)
        except IndexError:
            raise e.ParseError(module["installer"], rule_code=105)


def _install_steps(module, step_name):
    response = []
    try:
        for i in module[step_name]:
            response.append(c.run(i))
        return response
    except KeyError:
        return None


def _create_file(module):
    print(f"Creating file: {module['name']}...")
    return True


def _create_folder(module):
    print(f"Creating folder: {module['name']}...")
    return True


function = {"module": _install_module, "file": _create_file, "folder": _create_folder}
