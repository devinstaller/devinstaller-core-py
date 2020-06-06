# -----------------------------------------------------------------------------
# Created: Sun 24 May 2020 20:45:00 IST
# Last-Updated: Sat  6 Jun 2020 19:47:19 IST
#
# __init__.py is part of somepackge
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Init everything
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

"""Init everything"""

from devinstaller import yaml_handler as y
from devinstaller import installer as i
from devinstaller import commands as c
from devinstaller import schema as s
from devinstaller import exceptions as e
from devinstaller import helpers as h
from devinstaller import data


def validate_spec(doc_file_path: str, schema_file_path: str) -> dict:
    """Validate the spec

    Args:
        doc_file_path: The path to the devfile
        schema_file_path: The path to where the actual schema file lies

    Returns:
        Valid schema file
    """
    schema = y.read(schema_file_path)
    document = y.read(doc_file_path)
    return s.validate(document, schema)


def install(file_name: str, platform: str = None, preset: str = None) -> None:
    """Entry point for the install function

    Args:
        file_name: name of the devfile
        platform: name of the platform
        preset: name of the preset
    """
    document = _get_platform_document(y.read(file_name), platform)
    graph = s.generate_dependency(document)
    requirements_list = _get_preset_requirements(document, preset)
    i.main(graph, requirements_list)


def _get_preset_data(document, preset_name, rule_code):
    for preset in document["presets"]:
        if preset["name"] == preset_name:
            return preset
    raise e.RuleViolation(rule_code, data.rules[rule_code])


def _get_platform_document(document, platform):
    for _platform in document["platforms"]:
        if platform and _platform["name"] == platform:
            return _platform
        if version_compare(i):
            return _platform
    raise e.RuleViolation(100, data.rules[100])


def _get_preset_requirements(document, preset):
    if preset:
        return _get_preset_data(document, preset, 102)
    if h.check_key("default", document):
        return _get_preset_data(document, document["default"], 103)
    raise e.RuleViolation(101, data.rules[101])


def version_compare(input_data: dict) -> bool:
    """Check if the given platform is the one expected.
    It runs the command and checks it with the expected response in the
    devfile. If matches then it returns true else false.

    Args:
        input_data: The platform object in the devfile

    Returns:
        If present then True
    """
    command_response = c.run(input_data["version"]["command"])
    return bool(input_data["version"]["identifier"] == command_response["stdout"])
