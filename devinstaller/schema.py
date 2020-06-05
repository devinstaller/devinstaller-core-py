# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Fri  5 Jun 2020 18:51:12 IST
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

import cerberus
from devinstaller import exceptions as e


def validate(document, schema):
    """Validate and returns a sanitised document
    :param dict document: Python object which has to be validated
    :param dict schema: Python object against which to be validated
    :return: Sanitised object
    :rtype: dict
    """
    _v = cerberus.Validator(schema)
    if _v.validate(document):
        return _v.document
    raise e.SchemaComplianceError(_v.errors)


def _list_to_dict(input_data, key, module_type, installer=None):
    response = {}
    for i in input_data[key]:
        name = _get_name(i)
        response[name] = i
        response[name]["installed"] = False
        response[name]["type"] = module_type
        response[name] = _add_installer(response[name], installer)
    return response


def _add_installer(data, installer):
    if installer:
        data["installer"] = installer
    return data


def _get_name(input_data):
    if "alias" in input_data:
        return input_data["alias"]
    return input_data["name"]


def generate_dependency(input_data):
    """Generate dependency list(graph) from the data.
    Dependency list houses all the modules and their dependency on each other
    :param dict input_data: Data from which the graph is to be created
    :return: Dependency object
    :rtype: dict
    """
    response = {}
    response.update(
        _list_to_dict(input_data, "modules", "module", input_data["installer"])
    )
    response.update(_list_to_dict(input_data, "folders", "folder"))
    response.update(_list_to_dict(input_data, "files", "file"))
    return response
