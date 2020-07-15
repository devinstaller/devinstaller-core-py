# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Tue 14 Jul 2020 18:49:20 IST
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
        if platform_object["name"] in temp["supported_platforms"]:
            # For mutation purpose we have to cast Mapping -> dict
            module_object = cast(dict, temp)
            code_name = module_object.get("alias", module_object["name"])
            module_object["display"] = module_object.get(
                "display", module_object["name"]
            )
            module_object["installed"] = False
            module_object["before"] = get_hook(module_object, platform_object, "before")
            module_object["after"] = get_hook(module_object, platform_object, "after")
            response[code_name] = m.Module(**module_object)
    return response


def get_hook(
    module_object: m.ModuleType, platform_object: m.PlatformType, hook: str
) -> str:
    """Returns the hook for the module.
    Works for both `before` and `after` hooks.

    Steps:
        1. Returns the hook in the module. If not present then
        2. Returns the hook in the platform_object. If not present then
        3. Returns None

    Args:
        module_object: The object whose hook is required
        platform_object: The object from where the fallback hook is extracted
        hook: The name of the hook
    """
    fallback_hook = f"{hook}_each"
    if hook in module_object:
        return module_object[hook]
    if fallback_hook in platform_object:
        return platform_object[fallback_hook]
    return None


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
    try:
        if not platform_code_name:
            current_platform = get_current_platform()
            platform_list = full_document["platforms"]
            return get_platform_object_using_system(platform_list, current_platform)
        return get_platform_object_from_codename(
            full_document["platforms"], platform_code_name
        )
        raise e.RuleViolationError(100)
    except KeyError:
        raise e.SchemaComplianceError(errors="platform object missing")


def get_platform_object_from_codename(
    platform_list: List[m.PlatformType], platform_code_name: str
) -> m.PlatformType:
    """Returns the platform object whose name matches the `platform_code_name`.

    Args:
        full_document: The full spec file
        platform_code_name: name of the platform
    """
    for _plat in platform_list:
        if _plat["name"] == platform_code_name:
            return _plat


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
    for p in platform_list:
        if compare_strings(p["platform_info"]["system"], current_platform["system"]):
            if "version" not in p["platform_info"]:
                platforms_supported.append(p)
            elif compare_version(
                current_platform["version"], p["platform_info"]["version"]
            ):
                platforms_supported.append(p)
    if len(platforms_supported) > 1:
        return ask_user_for_platform_object(platforms_supported)
    elif len(platforms_supported) < 1:
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
    option, index = pick.pick(options, title)
    click.secho(f"Nice choice: {option}", fg="green")
    return get_platform_object_from_codename(platforms_supported, option)


def compare_version(version: str, expected_version: str) -> bool:
    # TODO Improve version comparision logic
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
