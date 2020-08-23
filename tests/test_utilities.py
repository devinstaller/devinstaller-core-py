import pytest

from devinstaller_core import utilities as u


@pytest.fixture
def compare():
    return u.Compare().strings


class TestCompare:
    def test_no_arg(self, compare):
        assert compare() is False

    def test_one_arg(self, compare):
        assert compare("foo") is True

    def test_two_arg(self, compare):
        assert compare("foo", "Foo") is True

    def test_negative_arg(self, compare):
        assert compare("foo", "bar") is False
