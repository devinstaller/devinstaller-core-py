import pytest

from devinstaller import exceptions as e

expected_response_for_specification = """
Errors: test
I found a violation of code S100.
S100: Your devfile is not a valid.
"""

expected_response_for_devinstaller = """
Errors: test
I found a violation of code D100.
D100: Schema object not found.
"""


def test_specification():
    err = e.SpecificationError(error="test", error_code="S100", message="")
    assert expected_response_for_specification == str(err)


def test_devinstaller():
    err = e.DevinstallerError("test", error_code="D100")
    assert expected_response_for_devinstaller == str(err)


def test_specification_fail():
    with pytest.raises(e.DevinstallerError):
        e.SpecificationError("test", error_code="invalid error code")


def test_devinstaller_fail():
    with pytest.raises(e.DevinstallerError):
        e.DevinstallerError("test", error_code="invalid error code")
