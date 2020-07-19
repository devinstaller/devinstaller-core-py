from unittest.mock import Mock

import pytest

from devinstaller import app
from devinstaller import models as m


@pytest.fixture
def mock_questionary(mocker):
    return mocker.patch("questionary.checkbox")


def test_ask_user_for_req_list(mock_questionary, mocker):
    module_objects = [
        m.Module(
            "foo",
            "app",
            False,
            "foo alias",
            "Foo as displayed",
            description="Foo description",
        ),
        m.Module("bar", "app", False, "bar alias", "Bar as displayed"),
    ]
    response = app.ask_user_for_the_requirement_list(module_objects)
    expected_response = ["bar alias"]
    mock_questionary.assert_called_once()
    assert response == expected_response
