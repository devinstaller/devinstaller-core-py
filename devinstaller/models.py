# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Mon  6 Jul 2020 17:29:58 IST
#
# models.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Contains all the app data
#
# Copyright (c) 2020, Justin Kizhakkinedath
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

"""All the models including the schema as well as graph models"""

from typing import List, Optional, Dict, TypedDict
from dataclasses import dataclass


@dataclass
class Module:
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    name: str
    type: str
    installed: bool
    description: Optional[str] = None
    url: Optional[str] = None
    alias: Optional[str] = None
    display: Optional[str] = None
    command: Optional[str] = None
    config: Optional[List[str]] = None
    init: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    version: Optional[str] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None


#
class NameType(TypedDict):
    """Type declaration for the `name` block
    """

    alias: str
    name: str
    display: str


class ModuleType(TypedDict):
    """Type declaration for the `base` block
    """

    command: str
    after: str
    before: str
    config: List[str]
    init: List[str]
    optionals: List[str]
    owner: str
    parent_dir: str
    permission: str
    requires: List[str]
    type: str
    version: str


class PresetType(NameType):
    """Type declaration for the `preset` block
    """

    requires: List[str]
    optionls: List[str]


class PlatformInfo(TypedDict):
    """Type declaration for the platform info
    """

    system: str
    version: str
    architecture: str


class PlatformType(NameType):
    """Type declaration for the `platform` block
    """

    installer: str
    default: str
    platform_info: PlatformInfo
    presets: List[PresetType]
    modules: List[ModuleType]


class FullDocumentType(TypedDict):
    """Type declaration for the whole spec file
    """

    version: str
    platforms: List[PlatformType]


class CommandRunResponseType(TypedDict):
    """Type declaration for response from the `command.run`
    """

    args: List[str]
    returncode: int
    stdout: str
    stderr: str


class ModuleInstalledResponseType(TypedDict):
    """Type declaration for the response of the module install
    """

    init: Optional[List[CommandRunResponseType]]
    config: Optional[List[CommandRunResponseType]]
    command: Optional[CommandRunResponseType]


def _module_block():
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "type": {
                    "type": "string",
                    "default": "app",
                    "one_of": ["app", "file", "folder"],
                },
                "alias": {"type": "string"},
                "name": {"type": "string", "required": True},
                "executable": {"type": "string"},
                "description": {"type": "string"},
                "url": {"type": "string"},
                "display": {"type": "string"},
                "after": {"type": "string"},
                "before": {"type": "string"},
                "command": {"type": ["string", "boolean"]},
                "config": {"type": "list", "schema": {"type": "string"}},
                "init": {"type": "list", "schema": {"type": "string"}},
                "optionals": {"type": "list", "schema": {"type": "string"}},
                "owner": {"type": "string"},
                "parent_dir": {"type": "string"},
                "permission": {"type": "string"},
                "requires": {"type": "list", "schema": {"type": "string"}},
                "version": {"type": "string"},
            },
        },
    }
    return data


def _preset_block():
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "requires": {"type": "list", "schema": {"type": "string"}},
                "optionals": {"type": "list", "schema": {"type": "string"}},
            },
        },
    }
    return data


def _platform_block():
    preset = _preset_block()
    module = _module_block()
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "default": {"type": "string"},
                "before_each": {"type": "string"},
                "after_each": {"type": "string"},
                "platform_info": {
                    "type": "dict",
                    "schema": {
                        "system": {"type": "string"},
                        "version": {"type": "string"},
                        "architecture": {"type": "string"},
                    },
                },
                "presets": preset,
                "modules": module,
            },
        },
    }
    return data


def schema() -> Dict:
    """Returns the schema object for validating the devfile

    Returns:
      A new instance of schema object
    """
    platform = _platform_block()
    data = {
        "version": {"type": "string"},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "url": {"type": "string"},
        "platforms": platform,
    }
    return data
