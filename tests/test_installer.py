import shlex

import pytest

from devinstaller import installer as i
from devinstaller import models as m


def test_install_module__skip():
    mock_data = {
        "alias": "mod",
        "name": "module1",
        "display": "module v1",
        "module_type": "app",
        "command": None,
    }
    mock_data = m.Module(**mock_data)
    i.install_module(mock_data)


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
    i.install_module(mock_data)


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


@pytest.fixture
def mock_module_map():
    module_map = {
        "a": m.Module(
            name="a", module_type="app", requires=["c"], alias="a", display="a"
        ),
        "b": m.Module(
            name="b", module_type="app", optionals=["d"], alias="b", display="b"
        ),
        "c": m.Module(name="c", module_type="app", alias="c", display="c"),
        "d": m.Module(name="d", module_type="app", alias="d", display="d"),
    }
    return module_map


class TestTraverse:
    def test_1(self, mock_module_map):
        i.main(module_map=mock_module_map, requirements_list=["a"])
        assert "success" == mock_module_map["a"].status
        assert None == mock_module_map["b"].status
        assert "success" == mock_module_map["c"].status
        assert None == mock_module_map["d"].status
