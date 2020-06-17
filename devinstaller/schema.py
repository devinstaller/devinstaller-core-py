# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Wed 17 Jun 2020 03:09:26 IST
#
# schema.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description:
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

"""Handles everything related to spec file schema"""

import cerberus
from devinstaller import exceptions as e
from devinstaller import models as m
from typing import Dict, Optional, Union, cast
import copy


def validate(document: dict) -> m.FullDocumentType:
    """Validate and returns a sanitised document

    Args:
        document: Python object which has to be validated

    Returns:
        Sanitised object
    """
    _v = cerberus.Validator(m.schema())
    if _v.validate(document):
        return _v.document
    raise e.SchemaComplianceError(_v.errors)


def _parse_installer_command(full_data: m.PlatformType, module_data: m.AppType) -> str:
    """Runs only in the case where there is no special command to install
    the module and where the default command will be used.

    Args:
        full_data: The whole spec for the current platform
        module_data: The data for the current module

    Returns:
        The command which will be used to install the module
    """
    try:
        return full_data["installer"].format(name=module_data["name"])
    except KeyError:
        raise e.ParseError(full_data["installer"], 105)


def _get_installer_command(input_data: m.PlatformType, data: dict,) -> Optional[str]:
    """Checks if the module is AppType and then proceeds to extract the
    installer command

    Args:
        input_data: The data specific to the platform
        data: Module data. Type: dict

    Returns:
        string containing the final command to install the app
    """
    if data["type"] == "app":
        # Reverting back type: dict -> AppType
        return _get_installer(input_data, cast(m.AppType, data))
    return None


def _get_installer(full_data: m.PlatformType, module_data: m.AppType) -> Optional[str]:
    """Gets the command which will be used to install the module

    Args:
        full_data: The whole spec for the current platform
        module_data: The data for the current module

    Returns:
        The command which will be used to install the module
    """
    if "command" in module_data:
        return module_data["command"] if module_data["command"] is not True else None
    if "installer" in full_data:
        return _parse_installer_command(full_data, module_data)
    raise e.RuleViolation(106)


def _list_to_dict(
    input_data: m.PlatformType, key: m.ModuleKeys
) -> Dict[str, m.CommonModule]:
    """Takes in the whole data and creates the dependency graph for one module_type

    Args:
        input_data: The whole spec for the current platform
        key: The name of the list which is to be serialised.
            Options: `apps`, `files` and `folders`.

    Returns:
        The graph for one specific platform
    """
    type_reference = {"apps": "app", "files": "file", "folders": "folder"}
    module_type = type_reference[key]
    response = {}
    for temp in input_data[key]:
        # For mutation purpose we have to cast Mapping -> dict
        data = cast(dict, temp)
        code_name = data.get("alias", data["name"])
        data["display"] = data.get("name", None)
        data["installed"] = False
        data["type"] = module_type
        data["command"] = _get_installer_command(input_data, data)
        response[code_name] = m.CommonModule(**data)
    return response


def generate_dependency(input_data: m.PlatformType) -> Dict[str, m.CommonModule]:
    """Generate dependency list(graph) from the data.
    Dependency list houses all the modules and their dependency on each other

    Args:
        input_data: Data from which the graph is to be created

    Returns:
        Dependency object
    """
    response = {}
    response.update(_list_to_dict(input_data, "apps"))
    response.update(_list_to_dict(input_data, "folders"))
    response.update(_list_to_dict(input_data, "files"))
    return response
