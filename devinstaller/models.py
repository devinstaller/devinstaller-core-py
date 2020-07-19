# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Sun 19 Jul 2020 18:52:35 IST
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
from typing import Any, Dict, List, NewType, Optional, TypedDict, Union


@dataclass
class ModuleInstallInstruction:
    """The class used to serialize`init`, `command` and `config` commands into objects
    """

    install: str
    rollback: Optional[str] = None


@dataclass
class Module:
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    name: str
    module_type: str
    installed: bool
    alias: str
    display: str
    command: Optional[ModuleInstallInstruction] = None
    config: Optional[List[ModuleInstallInstruction]] = None
    content: Optional[str] = None
    description: Optional[str] = None
    executable: Optional[str] = None
    init: Optional[List[ModuleInstallInstruction]] = None
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


class ModuleInstallInstructionType(TypedDict):
    """Type declaration for the instruction for `init`, `command` and `config`
    """

    install: str
    rollback: Optional[str]


class ModuleType(TypedDict):
    """Type declaration for all the block
    """

    alias: str
    init: List[Union[ModuleInstallInstructionType, str]]
    command: Union[ModuleInstallInstructionType, str]
    config: List[Union[ModuleInstallInstructionType, str]]
    content: str
    description: str
    display: str
    name: str
    executable: str
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


class ValidateResponseType(TypedDict):
    """Type declaration for the response of the `devinstaller.schema.validate` function
    """

    valid: bool
    document: Dict[Any, Any]
    errors: Dict[Any, Any]


ModuleMapType = NewType("ModuleMapType", Dict[str, Module])


def module() -> Dict[str, Any]:
    """
    Returns:
        The schema for the `module` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "module_type": {
                    "type": "string",
                    "default": "phony",
                    "allowed": ["app", "file", "folder", "link", "group", "phony"],
                },
                "supported_platforms": {"type": "list", "schema": {"type": "string"}},
                "alias": {"type": "string"},
                "create": {"type": "boolean"},
                "init": {
                    "type": "list",
                    "schema": {
                        "type": ["string", "dict"],
                        "schema": {
                            "install": {"type": "string"},
                            "rollback": {"type": "string"},
                        },
                    },
                },
                "command": {
                    "type": ["string", "dict"],
                    "schema": {
                        "install": {"type": "string"},
                        "rollback": {"type": "string"},
                    },
                },
                "config": {
                    "type": "list",
                    "schema": {
                        "type": ["string", "dict"],
                        "schema": {
                            "install": {"type": "string"},
                            "rollback": {"type": "string"},
                        },
                    },
                },
                "content": {"type": "string"},
                "description": {"type": "string"},
                "display": {"type": "string"},
                "executable": {"type": "string"},
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


def platform() -> Dict[str, Any]:
    """
    Returns:
        The schema for the `platform` block
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


def interface() -> Dict[str, Any]:
    """
    Returns:
      The schema for the `interface` block
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
                # `requires` other interface
                "requires": {"type": "list", "schema": {"type": "string"}},
                "before_each": {"type": "string"},
                "after_each": {"type": "string"},
                "modules": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"type": "string"},
                            "before": {"type": "string"},
                            "after": {"type": "string"},
                        },
                    },
                },
            },
        },
    }
    return data


def top_level() -> Dict[str, Any]:
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
    }
    return data


def schema() -> Dict[str, Any]:
    """Used for getting a new instance of the schema for the validating the spec file.

    Returns:
      The schema for the whole spec
    """
    data = dict(**top_level())
    data["platforms"] = platform()
    data["modules"] = module()
    data["interfaces"] = interface()
    return data
