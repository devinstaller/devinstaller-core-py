import pytest
from devinstaller import installer as i
from devinstaller import exceptions as e
import shlex


def test_install_command_skip():
    mock_data = {
        "name": "module1",
        "installer": "brew install {module_name}",
        "command": None,
    }
    response = i._install_module(mock_data)
    assert response["command"] == None


def test_install_command_custom(fake_process):
    command = "custom build --args1 arg1 --args2 arg2"
    mock_response = "Build success. All good"
    mock_command = shlex.split(command)
    fake_process.register_subprocess(mock_command, stdout=mock_response)
    mock_data = {
        "name": "module1",
        "installer": "brew install {module_name}",
        "command": command,
    }
    response = i._install_module(mock_data)
    assert response["command"]["stdout"] == mock_response


def test_install_command_default(fake_process):
    command = "brew install module1"
    mock_response = "Build success. All good"
    mock_command = shlex.split(command)
    fake_process.register_subprocess(mock_command, stdout=mock_response)
    mock_data = {
        "name": "module1",
        "installer": "brew install {name}",
    }
    response = i._install_module(mock_data)
    assert response["command"]["stdout"] == mock_response


def test_install_command_default_parse_error():
    mock_data = {
        "name": "module1",
        "installer": "brew install {}",
    }
    with pytest.raises(e.ParseError):
        i._install_module(mock_data)
