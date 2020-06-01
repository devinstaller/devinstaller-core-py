# -----------------------------------------------------------------------------
# Created: Mon  1 Jun 2020 14:12:09 IST
# Last-Updated: Tue  2 Jun 2020 01:13:15 IST
#
# installer.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Everything related to installer
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
from devinstaller import commands as c
from devinstaller import data
import devinstaller as d


def init(raw_document, platform=None, preset=None):
    document = get_platform_document(raw_document, platform)
    requirements_list = get_preset_requirements(document, preset)
    graph = s.generate_dependency(document)
    for module_name in requirements_list["requires"]:
        traverse(graph, module_name)


def traverse(graph, module_name):
    if not graph[module_name]["installed"]:
        execute(module_name, graph)
        graph[module_name]["installed"] = True
        if d.check_key("requires", graph[module_name]):
            for neighbour in graph[module_name]["requires"]:
                traverse(graph, neighbour)


def execute(module_name, graph):
    if d.check_key(module_name, graph):
        module = graph[module_name]
        if module["type"] == "module":
            print(f"Installing module: {module['name']}...")
            return True
        elif module["type"] == "folder":
            print(f"Creating folder: {module['name']}...")
            return True
        else:
            print(f"Creating file: {module['name']}...")
            return True
    else:
        print(f"I was unable to find the module: {module_name}")
        sys.exit(data.rules["104"])


def get_preset_requirements(document, preset):
    if not preset and not d.check_key("default", document):
        sys.exit(data.rules["101"])
    elif preset:
        return get_preset_data(document, preset, data.rules["102"])
    elif d.check_key("default", document):
        return get_preset_data(document, document["default"], data.rules["103"])


def get_preset_data(document, preset_name, rule):
    for i in document["presets"]:
        if i["name"] == preset_name:
            return i
    else:
        sys.exit(rule)


def get_platform_document(document, platform):
    for i in document["platforms"]:
        if platform and i["name"] == platform:
            return i
        elif version_compare(i):
            return i
    else:
        sys.exit(data.rules["100"])


def version_compare(data):
    command_response = c.run(data["version"]["command"])
    if (
        data["version"]["identifier"]
        == command_response.stdout.decode("utf-8").rstrip()
    ):
        return True
    else:
        return False
