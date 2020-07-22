import pytest

from devinstaller import app
from devinstaller import models as m


@pytest.fixture
def mock_questionary(mocker):
    return mocker.patch("devinstaller.utilities.ask_user_for_multi_select")


@pytest.fixture
def mock_module_objects():
    module_objects = [
        m.Module(
            name="foo",
            module_type="app",
            alias="foo alias",
            display="Foo as displayed",
            description="Foo description",
        ),
        m.Module(
            name="bar", module_type="app", alias="bar alias", display="Bar as displayed"
        ),
    ]
    return module_objects


def test_ask_user_for_req_list(mock_questionary, mock_module_objects):
    mock_questionary.return_value = ["Bar as displayed"]
    actual_response = app.ask_user_for_the_requirement_list(mock_module_objects)
    expected_response = ["bar alias"]
    assert expected_response == actual_response
