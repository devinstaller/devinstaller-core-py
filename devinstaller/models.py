# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Thu 16 Jul 2020 20:18:03 IST
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
from dataclasses import dataclass
from typing import Dict, List, Optional, TypedDict


@dataclass
class Module:
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    name: str
    module_type: str
    installed: bool
    codename: str
    display: str
    command: Optional[str] = None
    config: Optional[List[str]] = None
    content: Optional[str] = None
    description: Optional[str] = None
    executable: Optional[str] = None
    init: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
    requires: Optional[List[str]] = None
    url: Optional[str] = None
    version: Optional[str] = None
    source: Optional[str] = None
    target: Optional[str] = None
    symbolic: Optional[bool] = None


#
class ModuleType(TypedDict):
    """Type declaration for all the block
    """

    alias: str
    command: str
    config: List[str]
    content: str
    description: str
    display: str
    executable: str
    init: List[str]
    name: str
    optionals: List[str]
    owner: str
    parent_dir: str
    permission: str
    requires: List[str]
    module_type: str
    url: str
    version: str
    supported_platforms: List[str]
    source: str
    target: str
    symbolic: bool


class InterfaceModuleType(TypedDict):
    """Type declaration for the `modules` in the interface block
    """

    name: str
    before: str
    after: str


class InterfaceType(TypedDict):
    """Type declaration for the interface block
    """

    name: str
    description: str
    supported_platforms: List[str]
    before: str
    after: str
    requires: List[str]
    before_each: str
    after_each: str
    modules: List[InterfaceModuleType]


class PlatformInfoType(TypedDict):
    """Type declaration for the platform info
    """

    system: str
    version: str


class PlatformType(TypedDict):
    """Type declaration for the `platform` block
    """

    name: str
    description: str
    platform_info: PlatformInfoType


class PlatformIncludeType(TypedDict):
    """Type declaration for the platform include block
    """

    spec_file: str
    prog_file: str


class FullDocumentType(TypedDict):
    """Type declaration for the whole spec file
    """

    version: str
    author: str
    description: str
    url: str
    prog_file: str
    include: List[PlatformIncludeType]
    platforms: List[PlatformType]
    modules: List[ModuleType]
    interface: List[InterfaceType]


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


def module():
    """Return the schema for the `module` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "module_type": {
                    "type": "string",
                    "default": "app",
                    "one_of": ["app", "file", "folder", "link", "group"],
                },
                "supported_platforms": {"type": "list", "schema": {"type": "string"}},
                "alias": {"type": "string"},
                "command": {"type": ["string", "boolean"]},
                "config": {"type": "list", "schema": {"type": "string"}},
                "content": {"type": "string"},
                "description": {"type": "string"},
                "display": {"type": "string"},
                "executable": {"type": "string"},
                "init": {"type": "list", "schema": {"type": "string"}},
                "name": {"type": "string", "required": True},
                "optionals": {"type": "list", "schema": {"type": "string"}},
                "owner": {"type": "string"},
                "parent_dir": {"type": "string"},
                "permission": {"type": "string"},
                "requires": {"type": "list", "schema": {"type": "string"}},
                "url": {"type": "string"},
                "version": {"type": "string"},
                "source": {"type": "string"},
                "target": {"type": "string"},
                "symbolic": {"type": "boolean"},
            },
        },
    }
    return data


def platform():
    """Return the schema for the `platform` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "platform_info": {
                    "type": "dict",
                    "schema": {
                        "system": {"type": "string", "required": True},
                        "version": {"type": "string"},
                    },
                },
            },
        },
    }
    return data


def interface():
    """Return the schema for the `interface` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "supported_platforms": {"type": "list", "schema": {"type": "string"}},
                "before": {"type": "string"},
                "after": {"type": "string"},
                "requires": {"type": "list", "schema": {"type": "string"}},
                "before_each": {"type": "string"},
                "after_each": {"type": "string"},
                "modules": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": "string",
                            "before": "string",
                            "after": "string",
                        },
                    },
                },
            },
        },
    }
    return data


def schema() -> Dict:
    """Returns the schema object for validating the devfile

    Returns:
      A new instance of schema object
    """
    data = {
        "version": {"type": "string"},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "url": {"type": "string"},
        "include": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "spec_file": {"type": "string", "required": True},
                    "prog_file": {"type": "string"},
                },
            },
        },
        "prog_file": {"type": "string"},
        "platforms": platform(),
        "modules": module(),
        "interface": interface(),
    }
    return data
