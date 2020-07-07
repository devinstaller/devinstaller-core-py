# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Mon  6 Jul 2020 16:14:59 IST
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
from typing import Dict, cast

import cerberus

from devinstaller import exceptions as e
from devinstaller import models as m


def validate(document: dict) -> m.FullDocumentType:
    """Validate and returns a sanitised document

    Args:
        document: Python object which has to be validated

    Returns:
        Sanitised object
    """
    _v = cerberus.Validator(m.schema())
    if _v.validate(document):
        return _v.document
    raise e.SchemaComplianceError(_v.errors)


def generate_dependency(input_data: m.PlatformType) -> Dict[str, m.Module]:
    """Generate dependency list(graph) from the data.
    Dependency list houses all the modules and their dependency on each other

    Args:
        input_data: Data from which the graph is to be created

    Returns:
        Dependency object
    """
    response = {}
    for temp in input_data["modules"]:
        # For mutation purpose we have to cast Mapping -> dict
        data = cast(dict, temp)
        code_name = data.get("alias", data["name"])
        data["display"] = data.get("name")
        data["installed"] = False
        response[code_name] = m.Module(**data)
    return response
