import shlex

import pytest

from devinstaller import exceptions as e
from devinstaller import installer as i
from devinstaller import models as m


def test_install_module__skip():
    mock_data = {
        "alias": "mod",
        "name": "module1",
        "display": "module v1",
        "module_type": "app",
    }
    mock_data = m.Module(**mock_data)
    response = i.install_module(mock_data)
    assert response["command"] is None


def test_install_module__success(fake_process):
    command = "custom build --args1 arg1 --args2 arg2"
    mock_response = "Build success. All good"
    mock_command = shlex.split(command)
    fake_process.register_subprocess(mock_command, stdout=mock_response)
    mock_data = {
        "alias": "mod",
        "name": "module1",
        "display": "module v1",
        "module_type": "app",
    }
    mock_data = m.Module(**mock_data)
    response = i.install_module(mock_data)
    assert response["command"]["stdout"] == mock_response


@pytest.fixture
def mock_init():
    return [m.ModuleInstallInstruction("a"), m.ModuleInstallInstruction("b")]


@pytest.fixture
def mock_command():
    return m.ModuleInstallInstruction("c")


class TestAppendUtility:
    def test_all_present(self, mock_init, mock_command):
        expected_response = [
            m.ModuleInstallInstruction("a"),
            m.ModuleInstallInstruction("b"),
            m.ModuleInstallInstruction("c"),
        ]
        breakpoint()
        actual_response = i.append_if_not_none(mock_init, mock_command)
        assert expected_response == actual_response

    def test_command_none(self, mock_init):
        mock_command = None
        expected_response = [
            m.ModuleInstallInstruction("a"),
            m.ModuleInstallInstruction("b"),
        ]
        actual_response = i.append_if_not_none(mock_init, mock_command)
        assert expected_response == actual_response

    def test_init_none(self, mock_command):
        mock_init = None
        expected_response = [m.ModuleInstallInstruction("c")]
        actual_response = i.append_if_not_none(mock_init, mock_command)
        assert expected_response == actual_response

    def test_all_none(self):
        mock_init = None
        mock_command = None
        expected_response = []
        actual_response = i.append_if_not_none(mock_init, mock_command)
        assert expected_response == actual_response
