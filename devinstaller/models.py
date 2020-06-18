# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Thu 18 Jun 2020 20:48:07 IST
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

from typing import List, Optional, Dict, TypedDict, Literal
from dataclasses import dataclass


@dataclass
class _VersionModule:
    """Class containing the info necessary to get the version info"""

    response: str
    command: str


@dataclass
class CommonModule:
    """Common class for all modules"""

    # pylint: disable=too-many-instance-attributes
    name: str
    type: str
    installed: bool
    alias: Optional[str] = None
    display: Optional[str] = None
    command: Optional[str] = None
    config: Optional[List[str]] = None
    init: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    version: Optional[_VersionModule] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None


class NameType(TypedDict):
    """Type declaration for the `name` block
    """

    alias: str
    name: str
    display: str


class BaseType(TypedDict):
    """Type declaration for the `base` block
    """

    command: str
    requires: List[str]
    optionals: List[str]
    init: List[str]
    config: List[str]


class VersionType(TypedDict):
    """Type declaration for the `version` block
    """

    command: str
    response: str


class AppType(NameType, BaseType):
    """Type declaration for the `app` block
    """

    version: VersionType


class FileAndFolderType(NameType, BaseType):
    """Type declaration for the `file` and `folder` block
    """

    owner: str
    permission: str
    parent_dir: str


class PresetType(NameType):
    """Type declaration for the `preset` block
    """

    requires: List[str]
    optionls: List[str]


class PlatformType(NameType):
    """Type declaration for the `platform` block
    """

    installer: str
    default: str
    version: VersionType
    presets: List[PresetType]
    apps: List[AppType]
    files: List[FileAndFolderType]
    folders: List[FileAndFolderType]


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


ModuleKeys = Literal["apps", "files", "folders"]

# Elements are not mutated
def _name_element():
    return {
        "alias": {"type": "string"},
        "name": {"type": "string", "required": True},
        "display": {"type": "string"},
    }


def _base_element():
    return {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "requires": {"type": "list", "schema": {"type": "string"}},
                "optionals": {"type": "list", "schema": {"type": "string"}},
                "command": {"type": ["string", "boolean"]},
                "init": {"type": "list", "schema": {"type": "string"}},
                "config": {"type": "list", "schema": {"type": "string"}},
            },
        },
    }


def _version_element():
    return {
        "type": "dict",
        "schema": {
            "response": {"type": "string", "required": True},
            "command": {"type": "string", "required": True},
        },
    }


# Blocks returns separate copy of dict each time because they have to be mutated
def _preset_block():
    return {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "requires": {"type": "list", "schema": {"type": "string"}},
                "optionals": {"type": "list", "schema": {"type": "string"}},
            },
        },
    }


def _app_block(version):
    return {
        "type": "list",
        "schema": {"type": "dict", "schema": {"version": version}},
    }


def _file_and_folder_block():
    return {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "owner": {"type": "string"},
                "permission": {"type": "string"},
                "parent_dir": {"type": "string"},
            },
        },
    }


def _platform_block(version, preset, app, file_and_folder):
    return {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "default": {"type": "string"},
                "installer": {"type": "string"},
                "version": version,
                "presets": preset,
                "apps": app,
                "folders": file_and_folder,
                "files": file_and_folder,
            },
        },
    }


def _schema(platform):
    return {
        "version": {"type": "string"},
        "platforms": platform,
    }


def schema() -> Dict:
    """Returns the schema object for validating the devfile

    Returns:
      A new instance of schema object
    """
    # Creating new elements
    name = _name_element()
    private_name = _name_element()
    version = _version_element()
    # Building a new base element for other blocks
    base = _base_element()
    private_name["display"]["type"] = ["string", "boolean"]
    base["schema"]["schema"].update(private_name)
    # Update preset block
    preset = _preset_block()
    preset["schema"]["schema"].update(name)
    # Update app block
    app = _app_block(version)
    app["schema"]["schema"].update(base["schema"]["schema"])
    # Update file_and_folder block
    file_and_folder = _file_and_folder_block()
    file_and_folder["schema"]["schema"].update(base["schema"]["schema"])
    # Create a platform block using all the other blocks
    platform = _platform_block(
        version=version, preset=preset, app=app, file_and_folder=file_and_folder
    )
    platform["schema"]["schema"].update(name)
    # Creating and returning the schema
    return _schema(platform)
