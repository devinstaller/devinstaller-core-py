import os

import pytest
from hypothesis import given
from hypothesis_fspaths import fspaths

from devinstaller_core import file_manager as f

HOME_DIR = "/foo/bar"
CWD = "/foo/bar/baz"


@pytest.fixture
def mocked_open(mocker):
    """Mocking builtin open"""
    return mocker.patch("builtins.open")


@pytest.fixture
def mocked_home_dir(mocker):
    """Mocking home dir"""
    os.environ["HOME"] = HOME_DIR


@pytest.fixture
def mocked_cwd(mocker):
    """Mocking cwd"""
    mock = mocker.patch("os.getcwd")
    mock.return_value = CWD
    return mock


@pytest.fixture
def mocked_requests(mocker):
    """Mocking requests.get for the download feature"""
    mock = mocker.patch("requests.get")
    return mock


class TestFileManager:
    @pytest.mark.parametrize(
        "path, expected_response",
        [
            ("../temp/test.toml", f"{HOME_DIR}/temp/test.toml"),
            ("../test.toml", f"{HOME_DIR}/test.toml"),
            ("./temp/test.toml", f"{CWD}/temp/test.toml"),
            ("./test.toml", f"{CWD}/test.toml"),
            ("/temp/test.toml", f"/temp/test.toml"),
            ("/test.toml", f"/test.toml"),
            ("~/temp/test.toml", f"{HOME_DIR}/temp/test.toml"),
            ("~/test.toml", f"{HOME_DIR}/test.toml"),
            ("temp/test.toml", f"{CWD}/temp/test.toml"),
            ("test.toml", f"{CWD}/test.toml"),
        ],
    )
    def test_read(
        self, mocked_open, mocked_home_dir, mocked_cwd, path, expected_response
    ):
        f.FileManager.read(path)
        mocked_open.assert_called_with(expected_response, "r")

    @pytest.mark.parametrize("url", [("https://foo.bar.com/test.toml")])
    def test_download(self, mocked_requests, url):
        f.FileManager.download(url)
        mocked_requests.assert_called_with(url)

    @pytest.mark.parametrize("file_content, file_path", [("test data", "test.toml")])
    def test_save(self, mocked_open, file_content, file_path):
        f.FileManager.save(file_content, file_path)
        mocked_open.assert_called_with(file_path, "w")

    def test_hash(self):
        response = f.FileManager.hash_data("test")
        assert (
            response
            == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        )


@pytest.mark.xfail
class TestDevfileManager:
    def test_init(self):
        assert False

    def test_check_path(self):
        assert False

    def test_parse(self):
        assert False
