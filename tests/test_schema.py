# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 18:39:27 IST
# Last-Updated: Sun 23 Aug 2020 20:56:41 IST
#
# test_schema.py is part of devinstaller
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
import json

import pytest

from devinstaller_core import common_models as cm
from devinstaller_core import file_manager as f
from devinstaller_core import schema as s


@pytest.fixture(scope="class")
def schema():
    return cm.schema()


def read_json(file_path: str):
    with open(file_path, "r") as f:
        return json.loads(f.read())


class TestValidator:
    def test_top_level_success(self):
        document = read_json("tests/data/schema/top_level_valid.json")
        assert s.validate(document, cm.schema())["valid"]

    def test_top_level_fail(self):
        document = read_json("tests/data/schema/top_level_invalid.json")
        assert not s.validate(document, cm.schema())["valid"]

    def test_platform_success(self):
        document = read_json("tests/data/schema/platform_valid.json")
        assert s.validate(document, cm.schema())["valid"]

    def test_module_success(self):
        document = read_json("tests/data/schema/module_valid.json")
        assert s.validate(document, cm.schema())["valid"]

    def test_interface_success(self):
        document = read_json("tests/data/schema/interface_valid.json")
        assert s.validate(document, cm.schema())["valid"]

    def test_full_document_success(self):
        document = read_json("tests/data/schema/full_document_valid.json")
        assert s.validate(document, cm.schema())["valid"]
