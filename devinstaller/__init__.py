# -----------------------------------------------------------------------------
# Created: Sun 24 May 2020 20:45:00 IST
# Last-Updated: Tue  2 Jun 2020 01:12:57 IST
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

import sys
from devinstaller import yaml_handler as y
from devinstaller import installer as i
from devinstaller import schema as s


def validate_spec(doc_file_path, schema_file_path):
    schema = y.read(schema_file_path)
    document = y.read(doc_file_path)
    return s.validate(document, schema)


def install(file_name, platform=None, preset=None):
    raw_document = y.read(file_name)
    i.init(raw_document, platform, preset)


def check_key(key, data):
    if key in data:
        return True
    else:
        return False
