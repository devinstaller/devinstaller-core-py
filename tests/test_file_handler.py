import pytest

from devinstaller import file_handler as f

mock_obj = {"1": "foo", "2": "bar", "3": "baz"}


@pytest.fixture
def mock_read(mocker):
    return mocker.patch("devinstaller.file_handler.read")


@pytest.fixture
def mock_path(mocker):
    return mocker.patch("os.path.expanduser")


@pytest.fixture
def mock_download(mocker):
    return mocker.patch("devinstaller.file_handler.download")


class TestParseAndDownload:
    def test_url(self, mock_download):
        f.parse_and_download("url: https://foo.com/bar/baz.toml")
        mock_download.assert_called_with("https://foo.com/bar/baz.toml")

    def test_local_short(self, mock_read, mock_path):
        mock_path.return_value = "/foo/bar/devfile.toml"
        f.parse_and_download("file: ~/devfile.toml")
        mock_path.assert_called_with("~/devfile.toml")
        mock_read.assert_called_with("/foo/bar/devfile.toml")

    def test_local_full(self, mock_read, mock_path):
        mock_path.return_value = "/foo/bar/devfile.toml"
        f.parse_and_download("file: /foo/bar/devfile.toml")
        mock_path.assert_called_with("/foo/bar/devfile.toml")
        mock_read.assert_called_with("/foo/bar/devfile.toml")
