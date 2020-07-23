# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Fri 24 Jul 2020 02:08:53 IST
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
from typing import Any, Dict, List, Optional, Union, cast

import cerberus
from typeguard import typechecked

# from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m
from devinstaller import utilities as u

DEVFILE_SCHEMA = m.schema()


@typechecked
def validate(
    document: Dict[Any, Any], schema: Dict[Any, Any] = DEVFILE_SCHEMA
) -> m.TypeValidateResponse:
    """Validate the given document with the schema

    TODO update docs

    Args:
        document: Python object which has to be validated
        schema: It can also take in custom schema for validation. Default is the Full file schema

    Returns:
        A dict with its validity, document and its errors.
    """
    _v = cerberus.Validator(schema)
    data: m.TypeValidateResponse = {
        "valid": _v.validate(document),
        "document": _v.document,
        "errors": _v.errors,
    }
    return data


@typechecked
def get_validated_document(
    document: Dict[Any, Any], schema: Dict[Any, Any] = m.schema()
) -> m.TypeFullDocument:
    """Validate the given document with the schema

    TODO update docs

    Args:
        document: Python object which has to be validated
        schema: It can also take in custom schema for validation. Default is the Full file schema

    Returns:
        Validated object

    Raises:
        SpecificationError
            with error code :ref:`error-code-100`
    """
    data = validate(document)
    if data["valid"]:
        return cast(m.TypeFullDocument, data["document"])
    raise e.SpecificationError(str(data["errors"]), "S100")


@typechecked
def get_platform_object(
    full_document: m.TypeFullDocument, platform_code_name: Optional[str] = None
) -> m.TypePlatform:
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
            current_platform = u.get_current_platform()
            platform_list = full_document["platforms"]
            return get_platform_object_using_system(platform_list, current_platform)
        return get_mock_platform_object()
    return get_platform_object_from_codename(
        full_document["platforms"], platform_code_name
    )


@typechecked
def get_mock_platform_object() -> m.TypePlatform:
    """Returns a mock platform object

    Returns:
        Mock platform object
    """
    return {
        "name": "MOCK",
        "description": "MOCK",
        "platform_info": {"system": "MOCK", "version": "MOCK"},
    }


@typechecked
def get_platform_object_from_codename(
    platform_list: List[m.TypePlatform], platform_codename: str
) -> m.TypePlatform:
    """Returns the platform object whose name matches the `platform_codename`.

    Args:
        full_document: The full spec file
        platform_codename: name of the platform

    Raises:
        SpecificationError
            with error code :ref:`error-code-S100`
    """
    for _plat in platform_list:
        if _plat["name"] == platform_codename:
            return _plat
    raise e.SpecificationError(platform_codename, "S100", "You are missing a platform")


@typechecked
def get_platform_object_using_system(
    platform_list: List[m.TypePlatform], current_platform: m.TypePlatformInfo
) -> m.TypePlatform:
    """Gets the current platform code name

    Args:
        platform_list: List of all platforms declared in the spec
        current_platform: The current platform object

    Returns:
        The `code_name` of current platform
    """
    platforms_supported: List[m.TypePlatform] = []
    for _p in platform_list:
        if u.compare_strings(_p["platform_info"]["system"], current_platform["system"]):
            if "version" not in _p["platform_info"]:
                platforms_supported.append(_p)
            elif u.compare_version(
                current_platform["version"], _p["platform_info"]["version"]
            ):
                platforms_supported.append(_p)
    if len(platforms_supported) == 1:
        print(f"I see you are using {platforms_supported[0]['name']}")
        return platforms_supported[0]
    return ask_user_for_platform_object(platforms_supported)


@typechecked
def ask_user_for_platform_object(
    platforms_supported: List[m.TypePlatform],
) -> m.TypePlatform:
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
    choices = [p["name"] for p in platforms_supported]
    selection = u.ask_user_to_select(title, choices)
    return get_platform_object_from_codename(platforms_supported, selection)
