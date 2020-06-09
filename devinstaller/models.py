# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Wed 10 Jun 2020 01:55:11 IST
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

from typing import List, Dict, Optional, Union
from dataclasses import dataclass, field, InitVar
from devinstaller import exception as e


def _get_value(
    input_data: Dict[str, str], key: str, default: str = None
) -> Optional[str]:
    try:
        return input_data[key]
    except KeyError:
        return default


@dataclass
class NameTag:
    """Class containing the name, alias and display"""

    name: str
    alias: str = None
    display: Optional[str] = None

    def __post_init__(self):
        if self.alias is None:
            self.alias = self.name


@dataclass
class BaseModule(NameTag):
    """Base class for all modules"""

    command: str = None
    config: Optional[List] = None
    init: Optional[List] = None
    optionals: Optional[List] = None
    requires: Optional[List] = None
    installer: InitVar[str] = None

    def __post_init__(self, installer):
        super(BaseModule, self).__post_init__()
        if self.command is None:
            if installer is not None:
                self.command = installer
            raise e.RuleViolation(rule_code=106)


# class AppModule(BaseModule):
#     """Class representing an app module"""

#     def __init__(self, input_data: Dict[str, str], installer: str):
#         self.executable = _get_value(input_data, "executable")
#         self.version = _get_value(input_data, "version")
#         super(AppModule, self).__init__(input_data, installer)

#     def __repr__(self):
#         return "This is app class"


# class FileFolderBaseModule(BaseModule):
#     """Base class for file and folder"""

#     def __init__(self, input_data: Dict[str, str], installer: str):
#         self.owner = _get_value(input_data, "owner")
#         self.parent_dir = _get_value(input_data, "parent_dir")
#         self.permission = _get_value(input_data, "permission")
#         super(FileFolderBaseModule, self).__init__(input_data, installer)


# class FileModule(FileFolderBaseModule):
#     """Class representing an file module"""

#     def __init__(self, input_data: Dict[str, str], installer: str):
#         super(FileModule, self).__init__(input_data, installer)


# class FolderModule(FileFolderBaseModule):
#     """Class representing an folder module"""

#     def __init__(self, input_data: Dict[str, str], installer: str):
#         super(FolderModule, self).__init__(input_data, installer)


# class PlatformModule(NameTag):
#     """Class representing an platform"""

#     def __init__(self, input_data: Dict[str, str], _):
#         installer = input_data["installer"]
#         version = input_data["version"]

#         self.default = _get_value(input_data, "default")
#         self.installer = _get_value(input_data, "installer")
#         self.version = {
#             "identifier": _get_value(version, "identifier"),
#             "command": _get_value(version, "command"),
#         }

#         self.presets = _serialize_list(input_data["presets"], "presets")

#         self.apps = _serialize_list(input_data, "apps", installer)
#         self.files = _serialize_list(input_data, "files", installer)
#         self.folders = _serialize_list(input_data, "folders", installer)
#         super(PlatformModule, self).__init__(input_data, installer)


# @dataclass
# class PresetModule(NameTag):
#     """Class representing preset"""

#     def __init__(self, input_data: Dict[str, str], _):
#         self.requires = _get_value(input_data, "requires")
#         self.optionals = _get_value(input_data, "optionals")
#         super(PresetModule, self).__init__(input_data)


# class SchemaModule:
#     """Class representing the devfile"""

#     def __init__(self, input_data: Dict[str, str]):
#         self.platforms = _serialize_list(input_data, "platforms")


# ListApp = List[AppModule]
# ListFile = List[FileModule]
# ListFolder = List[FolderModule]
# ModuleType = Union[ListApp, ListFile, ListFolder]


# def _serialize_list(
#     input_data: Dict[str, str], key: str, installer: str = None
# ) -> List[Union[[ModuleType], PlatformModule]]:
#     response: List[ModuleType] = []
#     ref = {
#         "platforms": PlatformModule,
#         "apps": AppModule,
#         "files": FileModule,
#         "folder": FolderModule,
#         "presets": PresetModule,
#     }
#     for mod in input_data[key]:
#         response.append(ref[key](mod, installer))
#     return response
