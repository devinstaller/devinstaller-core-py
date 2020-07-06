import shlex
import pytest
from devinstaller import installer as i
from devinstaller import exceptions as e
from devinstaller import models as m


def test_install_module__skip():
    mock_data = {
        "name": "module1",
        "type": "app",
        "installed": False,
        "command": None,
    }
    mock_data = m.Module(**mock_data)
    response = i._install_module(mock_data)
    assert response["command"] is None


def test_install_module__success(fake_process):
    command = "custom build --args1 arg1 --args2 arg2"
    mock_response = "Build success. All good"
    mock_command = shlex.split(command)
    fake_process.register_subprocess(mock_command, stdout=mock_response)
    mock_data = {
        "name": "module1",
        "type": "app",
        "installed": False,
        "command": command,
    }
    mock_data = m.Module(**mock_data)
    response = i._install_module(mock_data)
    assert response["command"]["stdout"] == mock_response
