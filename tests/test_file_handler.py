import pytest

from devinstaller import file_handler as f

mock_obj = {"1": "foo", "2": "bar", "3": "baz"}


@pytest.fixture
def mock_read(mocker):
    return mocker.patch("devinstaller.file_handler.read_file_and_parse")


@pytest.fixture
def mock_download(mocker):
    return mocker.patch("devinstaller.file_handler.download")


class TestParseAndDownload:
    def test_url(self, mock_download):
        f.check_and_download("url: https://foo.com/bar/baz.toml")
        mock_download.assert_called_with("https://foo.com/bar/baz.toml")

    def test_local(self, mock_read):
        f.check_and_download("file: ~/devfile.toml")
        mock_read.assert_called_with("~/devfile.toml")
