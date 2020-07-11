# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Sat 11 Jul 2020 20:17:33 IST
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


def generate_dependency(input_data: m.PlatformType) -> Dict[str, m.Module]:
    """Generate dependency list(graph) from the data.
    Dependency list houses all the modules and their dependency on each other

    Args:
        input_data: Data from which the graph is to be created

    Returns:
        Dependency object
    """
    response = {}
    for temp in input_data["modules"]:
        # For mutation purpose we have to cast Mapping -> dict
        data = cast(dict, temp)
        code_name = data.get("alias", data["name"])
        data["display"] = data.get("name")
        data["installed"] = False
        response[code_name] = m.Module(**data)
    return response


def extract(
    full_document: m.FullDocumentType,
    platform_code_name: Optional[str] = None,
    preset: Optional[str] = None,
    module: Optional[str] = None,
) -> None:
    """Entry point for schema extraction.
    Extraction involves parsing and figuring out the exact parameters required
    to proceed.

    Args:
        full_document: The full spec file
        platform: name of the platform
        preset: name of the preset
    """
    if not platform_code_name:
        if "platforms" in full_document:
            current_platform = get_current_platform()
            platform_list = full_document["platforms"]
            platform_code_name = get_platform_code_name(platform_list, current_platform)


def get_platform_code_name(
    platform_list: List[m.PlatformType], current_platform: m.PlatformInfoType
) -> str:
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
        return ask_user_for_platform(platforms_supported)
    elif len(platforms_supported) < 1:
        raise e.PlatformUnsupportedError
    return platforms_supported[0]["name"]


def ask_user_for_platform(platforms_supported: List[m.PlatformType]) -> str:
    print(
        "Hey.. your current platform supports multiple platforms declared in the spec file"
    )
    title = "Do you mind narrowring it down to one for me?"
    options = [p["name"] for p in platforms_supported]
    option, index = pick.pick(options, title)
    click.secho(f"Nice choice: {option}", fg="green")
    return option


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
