# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Mon 25 May 2020 17:54:59 IST
#
# schema.py is part of devin
# URL: https://gitlab.com/justinekizhak/devin
# Description:
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

import cerberus

def validate(document, schema):
    v = cerberus.Validator(schema)
    response = {
        "is_valid": v.validate(document),
        "errors": v.errors
    }
    return response

def _list_to_dict(input_data, key):
    response = {}
    for i in input_data[key]:
        response[_get_name(i)] = i
    return response

def _get_name(input_data):
    if "alias" in input_data:
        return input_data["alias"]
    else:
        return input_data["name"]


def _generate_dependency(input_data):
    response = {}
    response.update(_list_to_dict(input_data, "apps"))
    response.update(_list_to_dict(input_data, "folders"))
    response.update(_list_to_dict(input_data, "files"))
    return response

def generate_dependency(input_data):
    response = {}
    for i in input_data["platforms"]:
        response[_get_name(i)] = _generate_dependency(i)
    return response
