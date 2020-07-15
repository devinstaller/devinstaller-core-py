import pytest

import devinstaller as d


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
        response = d.get_current_platform()
        mocked_version.assert_called_once()
        mocked_mac_ver.assert_called_once()
        assert response == expected_response

    def test_others(self, mocked_mac_ver, mocked_system, mocked_version):
        expected_response = {"system": "Linux", "version": "10.14.6"}
        mocked_system.return_value = expected_response["system"]
        mocked_version.return_value = expected_response["version"]
        response = d.get_current_platform()
        mocked_mac_ver.assert_not_called()
        assert response == expected_response


class TestCompareStrings:
    def test_no_arg(self):
        assert d.compare_strings() is False

    def test_one_arg(self):
        assert d.compare_strings("foo") is True

    def test_two_arg(self):
        assert d.compare_strings("foo", "Foo") is True

    def test_negative_arg(self):
        assert d.compare_strings("foo", "bar") is False
