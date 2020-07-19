# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 18:39:27 IST
# Last-Updated: Sun 19 Jul 2020 19:10:20 IST
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
import pytest

from devinstaller import exceptions as e
from devinstaller import file_handler as f
from devinstaller import models as m
from devinstaller import schema as s


@pytest.fixture(scope="class")
def schema():
    return m.schema()


class TestSchemaValidity:
    def test_toplevel(self, schema):
        expected = f.read("tests/data/schema/top_level_schema.json")
        assert expected["version"] == schema["version"]
        assert expected["author"] == schema["author"]
        assert expected["description"] == schema["description"]
        assert expected["url"] == schema["url"]
        assert expected["include"] == schema["include"]
        assert expected["prog_file"] == schema["prog_file"]

    def test_platforms_block(self, schema):
        expected = f.read("tests/data/schema/platform_schema.json")
        assert expected == schema["platforms"]

    def test_modules_block(self, schema):
        expected = f.read("tests/data/schema/module_schema.json")
        assert expected == schema["modules"]

    def test_interfaces_block(self, schema):
        expected = f.read("tests/data/schema/interface_schema.json")
        assert expected == schema["interfaces"]


@pytest.fixture
def mocked_system(mocker):
    return mocker.patch("platform.system")


@pytest.fixture
def mocked_version(mocker):
    return mocker.patch("platform.version")


@pytest.fixture
def mocked_mac_ver(mocker):
    return mocker.patch("platform.mac_ver")


class TestGetCurrentPlatform:
    def test_mac(self, mocked_mac_ver, mocked_system, mocked_version):
        expected_response = {"system": "Darwin", "version": "10.10.10"}
        mocked_mac_ver_response = ("10.10.10", ("", "", ""), "x86_64")
        mocked_system.return_value = expected_response["system"]
        mocked_mac_ver.return_value = mocked_mac_ver_response
        response = s.get_current_platform()
        mocked_version.assert_called_once()
        mocked_mac_ver.assert_called_once()
        assert response == expected_response

    def test_others(self, mocked_mac_ver, mocked_system, mocked_version):
        expected_response = {"system": "Linux", "version": "10.14.6"}
        mocked_system.return_value = expected_response["system"]
        mocked_version.return_value = expected_response["version"]
        response = s.get_current_platform()
        mocked_mac_ver.assert_not_called()
        assert response == expected_response


class TestCompareStrings:
    def test_no_arg(self):
        assert s.compare_strings() is False

    def test_one_arg(self):
        assert s.compare_strings("foo") is True

    def test_two_arg(self):
        assert s.compare_strings("foo", "Foo") is True

    def test_negative_arg(self):
        assert s.compare_strings("foo", "bar") is False


@pytest.fixture
def full_document():
    return f.read("tests/data/module_map_1.toml")


class TestGenerateModuleMap:
    def test_1(self, full_document):
        """Testing if both foo and bar modules are returned.
        foo is explicity supported and bar is implicitly.
        """
        platform_object = {"name": "macos"}
        module_map = s.generate_module_map(full_document["modules"], platform_object)
        expected_response = {
            "foo": m.Module("foo", "app", False, "foo", "foo"),
            "bar": m.Module("bar", "app", False, "bar", "bar"),
        }
        assert module_map == expected_response

    def test_2(self, full_document):
        """Testing if only bar module is returned.
        foo is NOT supported and bar is supported implicitly.
        """
        platform_object = {"name": "test"}
        module_map = s.generate_module_map(full_document["modules"], platform_object)
        expected_response = {"bar": m.Module("bar", "app", False, "bar", "bar")}
        assert module_map == expected_response


class TestValidator:
    def test_top_level_success(self):
        document = f.read("tests/data/schema/top_level_valid.json")
        assert s.validate(document)["valid"]

    def test_top_level_fail(self):
        document = f.read("tests/data/schema/top_level_invalid.json")
        assert not s.validate(document, m.top_level())["valid"]

    def test_platform_success(self):
        document = f.read("tests/data/schema/platform_valid.json")
        assert s.validate(document)["valid"]

    def test_module_success(self):
        document = f.read("tests/data/schema/module_valid.json")
        assert s.validate(document)["valid"]

    def test_interface_success(self):
        document = f.read("tests/data/schema/interface_valid.json")
        assert s.validate(document)["valid"]

    def test_full_document_success(self):
        document = f.read("tests/data/schema/full_document_valid.json")
        assert s.validate(document)["valid"]
