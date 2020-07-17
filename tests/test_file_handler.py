import pytest

from devinstaller import file_handler as f

mock_obj = {"1": "foo", "2": "bar", "3": "baz"}


@pytest.fixture
def mock_read(mocker):
    return mocker.patch("devinstaller.file_handler.read")


@pytest.fixture
def mock_download(mocker):
    return mocker.patch("devinstaller.file_handler.download")


class TestParseAndDownload:
    def test_url(self, mock_download):
        response = f.parse_and_download(
            "url: https://gitlab.com/justinekizhak/dotfiles/-/raw/master/devfile.toml"
        )
        assert response == "url"

    def test_local_short(self, mock_file):
        response = f.parse_and_download("file: ~/devfile.toml")
        mock_file.assert_called

    def test_local_full(self, mock_file):
        response = f.parse_and_download("file: /Users/foo/devfile.toml")
        mock_file.assert_called
