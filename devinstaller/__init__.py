# -----------------------------------------------------------------------------
# Created: Sun 24 May 2020 20:45:00 IST
# Last-Updated: Fri 29 May 2020 16:45:49 IST
#
# __init__.py is part of somepackge
# URL: https://github.com/bast/somepackage
# Description: Init everything
#
# Copyright (c) 2020, Justine Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "software"), to deal
#   in the software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the software, and to permit persons to whom the software is
#   furnished to do so, subject to the following conditions:
#
#   the above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the software.
#
#   the software is provided "as is", without warranty of any kind,
#   express or implied, including but not limited to the warranties of
#   merchantability, fitness for a particular purpose and noninfringement.
#   in no event shall the authors or copyright holders be liable for any claim,
#   damages or other liability, whether in an action of contract, tort or
#   otherwise, arising from, out of or in connection with the software or the use
#   or other dealings in the software.
# -----------------------------------------------------------------------------

from devinstaller import schema as s
from devinstaller import yaml as y
from devinstaller import commands as c
import sys
from devinstaller import data

def validate_spec(doc_file_path, schema_file_path):
    schema = y.read(schema_file_path)
    document = y.read(doc_file_path)
    return s.validate(document, schema)


def install(file_name, platform=None, preset=None):
    raw_document = y.read(file_name)
    document = __get_platform_document(raw_document, platform)
    requirements_list = __get_preset_requirements(document, preset)
    dependency_list = s.generate_dependency(document)
    for module_name in requirements_list['requires']:
        _install(dependency_list, module_name)


def _install(dependency_list, module_name):
    if not dependency_list[module_name]["installed"]:
        __install(module_name, dependency_list)
        dependency_list[module_name]["installed"] = True
        if _check_key("requires", dependency_list[module_name]):
            for neighbour in dependency_list[module_name]['requires']:
                _install(dependency_list, neighbour)

def __install(module_name, dependency_list):
    if _check_key(module_name, dependency_list):
        module = dependency_list[module_name]
        if module['type'] == "module":
            print(f"Installing module: {module['name']}...")
            return True
        elif module['type'] == "folder":
            print(f"Creating folder: {module['name']}...")
            return True
        elif module['type'] == "file":
            print(f"Creating file: {module['name']}...")
            return True
    else:
        print(f"I was unable to find the module: {module_name}")
        sys.exit(data.rules["104"])

def _check_key(key, data):
    if key in data:
        return True
    else:
        return False

def __get_preset_requirements(document, preset):
    if not preset and not _check_key("default", document):
        sys.exit(data.rules["101"])
    elif preset:
        for i in document["presets"]:
            if i["name"] == preset:
                return i
        else:
            print(f"The preset you gave through cli was: {preset}")
            sys.exit(data.rules["102"])
    elif _check_key("default", document):
        for i in document["presets"]:
            if i["name"] == document["default"]:
                return i
        else:
            print(f"The default preset I found in the spec was : {document['default']}")
            sys.exit(data.rules["103"])


def __get_platform_document(document, platform):
    for i in document["platforms"]:
        if platform and i["name"] == platform:
            return i
        elif _version_compare(i):
            return i
    else:
        sys.exit(data.rules["100"])


def _version_compare(data):
    command_response = c.run(data["version"]["command"])
    if data["version"]["identifier"] == command_response.stdout.decode("utf-8").rstrip():
        return True
    else:
        return False
