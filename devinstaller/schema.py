# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Fri 17 Jul 2020 13:35:33 IST
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
import platform
from typing import Dict, List, Optional, cast

import cerberus
import click
import pick

# from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m


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


def generate_dependency(
    input_data: m.FullDocumentType, platform_object: m.PlatformType
) -> Dict[str, m.Module]:
    """Generate dependency list(graph) from the data.
    Dependency list houses all the modules and their dependency on each other

    Args:
        input_data: List of all modules
        platform_code_name: The name of the platform

    Returns:
        Dependency object for that specific platform
    """
    response = {}
    for temp in input_data["modules"]:
        if check_for_module_platform_compatibility(platform_object, temp):
            # For mutation purpose we have to cast Mapping -> dict
            module_object = cast(dict, temp)
            codename = module_object.get("alias", module_object["name"])
            module_object["display"] = module_object.get(
                "display", module_object["name"]
            )
            module_object["codename"] = codename
            module_object["installed"] = False
            response[codename] = m.Module(**module_object)
    return response


def check_for_module_platform_compatibility(
    platform_object: m.PlatformType, module: m.ModuleType
) -> bool:
    """Checks if the given module is compatible with the current platform.

    Steps:
        1. Checks if the user has provided `supported_platforms` key-value pair
        in the module object. If it is NOT provided then it is assumed that this specific
        module is compatible with all platforms and returns True.
        2. Checks if the platform object is a "mock" platform object or not.
        If the user didn't provided platforms block in the spec a "mock"
        platform object as placeholder is generated. So it checks whether is
        this the mock object or not. If it is then `SchemaComplianceError` is raised.
        3. Checks if the platform name is supported by the module. If yes then returns True.
        4. Nothing else then returns False

    Args:
        platform_object: The current platform object
        module: The module object

    Returns:
        True if compatible else False
    """
    if "supported_platforms" not in module:
        return True
    if platform_object["name"] == "MOCK":
        raise e.SchemaComplianceError(
            errors=(
                f"You used the `supported_platforms` key in {module['name']},"
                "but your spec file didn't have any `platforms` module."
            )
        )
    if platform_object["name"] in module["supported_platforms"]:
        return True
    return False


def get_platform_object(
    full_document: m.FullDocumentType, platform_code_name: Optional[str] = None
) -> m.PlatformType:
    """Main function to get the platform object.

    Steps:
        1. If `platform_code_name` is provided then that is used to get the platform object
        2. If not present then current platform is checked against all the platforms defined

    Args:
        full_document: The full spec file
        platform_code_name: name of the platform

    Returns:
        The platform object
    """
    if not platform_code_name:
        if "platforms" in full_document:
            current_platform = get_current_platform()
            platform_list = full_document["platforms"]
            return get_platform_object_using_system(platform_list, current_platform)
        return get_mock_platform_object()
    return get_platform_object_from_codename(
        full_document["platforms"], platform_code_name
    )


def get_mock_platform_object() -> m.PlatformType:
    """Returns a mock platform object

    Returns:
        Mock platform object
    """
    return {
        "name": "MOCK",
        "description": "MOCK",
        "platform_info": {"system": "MOCK", "version": "MOCK"},
    }


def get_platform_object_from_codename(
    platform_list: List[m.PlatformType], platform_codename: str
) -> m.PlatformType:
    """Returns the platform object whose name matches the `platform_codename`.

    Args:
        full_document: The full spec file
        platform_codename: name of the platform
    """
    for _plat in platform_list:
        if _plat["name"] == platform_codename:
            return _plat
    raise e.RuleViolationError(
        106, f"I couldn't find any platform called {platform_codename}"
    )


def get_platform_object_using_system(
    platform_list: List[m.PlatformType], current_platform: m.PlatformInfoType
) -> m.PlatformType:
    """Gets the current platform code name

    Args:
        platform_list: List of all platforms declared in the spec
        current_platform: The current platform object

    Returns:
        The `code_name` of current platform
    """
    platforms_supported: List[m.PlatformType] = []
    for _p in platform_list:
        if compare_strings(_p["platform_info"]["system"], current_platform["system"]):
            if "version" not in _p["platform_info"]:
                platforms_supported.append(_p)
            elif compare_version(
                current_platform["version"], _p["platform_info"]["version"]
            ):
                platforms_supported.append(_p)
    if len(platforms_supported) > 1:
        return ask_user_for_platform_object(platforms_supported)
    if len(platforms_supported) < 1:
        raise e.PlatformUnsupportedError
    return platforms_supported[0]


def ask_user_for_platform_object(
    platforms_supported: List[m.PlatformType],
) -> m.PlatformType:
    """Ask the user for which platform to be used.
    Sometimes it may happen that platform code name is not provided by the user so the
    system tries to figure which platform it is currently running.
    But it may happen that multiple platforms defined satisfy the conditions, in that case
    we will explicitly ask the user to select one of the platforms which are satisfied.

    Args:
        platforms_supported: List of platform objects which satisfies the condition

    Returns:
        The required platform object
    """
    print(
        'Hey.. your current platform supports multiple "platform" declared in the spec file'
    )
    title = "Do you mind narrowring it down to one for me?"
    options = [p["name"] for p in platforms_supported]
    option, _ = pick.pick(options, title)
    click.secho(f"Nice choice: {option}", fg="green")
    return get_platform_object_from_codename(platforms_supported, option)


def compare_version(version: str, expected_version: str) -> bool:
    """Compares the version of the current platform and the version info in the spec file.

    Works with both the platforms block and the modules block?

    Uses the semver specification to compare.
    """
    # TODO How to compare using the semver specification.
    # TODO What about the modules which doesnt' use the semver spec?
    if version == expected_version:
        return True
    return False


def compare_strings(*args: str) -> bool:
    """Compare all the strings with each other (case insensitive)

    Args:
        Any number of string arguments.
        At least one argument required else it will return False.
        If one argument then it will return True.

    Returns:
        True if all matches else False
    """
    if len({v.casefold() for v in args}) != 1:
        return False
    return True


def get_current_platform() -> m.PlatformInfoType:
    """Get the current platform object

    Returns:
        The current platform object
    """
    data: m.PlatformInfoType = {
        "system": platform.system(),
        "version": platform.version(),
    }
    if data["system"] == "Darwin":
        data["version"] = platform.mac_ver()[0]
    return data
