# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 18:39:27 IST
# Last-Updated: Thu 11 Jun 2020 20:34:30 IST
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

from devinstaller import schema as s
from devinstaller import yaml_handler as y
from devinstaller import exceptions as e
from devinstaller import models as m
import pytest


def test_validator_valid():
    expected_schema = y.read("tests/data/schema.yml")
    schema = m.schema()

    assert expected_schema["version"] == schema["version"]

    # Check presets structure
    expected_presets = expected_schema["platforms"]["schema"]["schema"]["presets"]
    schema_presets = schema["platforms"]["schema"]["schema"]["presets"]
    assert expected_presets == schema_presets

    # Check version structure
    expected_version = expected_schema["platforms"]["schema"]["schema"]["version"]
    schema_version = schema["platforms"]["schema"]["schema"]["version"]
    assert expected_version == schema_version

    # Check apps structure
    expected_apps = expected_schema["platforms"]["schema"]["schema"]["apps"]
    schema_apps = schema["platforms"]["schema"]["schema"]["apps"]
    assert expected_apps == schema_apps

    # Check files structure
    expected_files = expected_schema["platforms"]["schema"]["schema"]["files"]
    schema_files = schema["platforms"]["schema"]["schema"]["files"]
    assert expected_files == schema_files

    # Check folders structure
    expected_folders = expected_schema["platforms"]["schema"]["schema"]["folders"]
    schema_folders = schema["platforms"]["schema"]["schema"]["folders"]
    assert expected_folders == schema_folders

    # Check overall schema
    assert expected_schema == schema


def test_validator_invalid():
    document = y.read("tests/data/invalid_spec.yml")
    with pytest.raises(e.SchemaComplianceError):
        s.validate(document)
