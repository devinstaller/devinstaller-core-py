import pytest

from devinstaller_core import block_platform as s
from devinstaller_core import exception as e


@pytest.fixture
def mocked_system_mac(mocker):
    mock = mocker.patch("platform.system")
    mock.return_value = "Darwin"
    return mock


@pytest.fixture
def mocked_system_linux(mocker):
    mock = mocker.patch("platform.system")
    mock.return_value = "Linux"
    return mock


@pytest.fixture
def mocked_version_dummy(mocker):
    mock = mocker.patch("platform.version")
    mock.return_value = "test"
    return mock


@pytest.fixture
def mocked_version_linux(mocker):
    mock = mocker.patch("platform.version")
    mock.return_value = "10.14.6"
    return mock


@pytest.fixture
def mocked_mac_ver(mocker):
    mock = mocker.patch("platform.mac_ver")
    mock.return_value = ("10.10.10", ("", "", ""), "x86_64")
    return mock


@pytest.fixture
def mock_platform_list():
    return [
        {"name": "macos", "platform_info": {"system": "Darwin", "version": "10.10.10"}},
        {"name": "ubuntu", "platform_info": {"system": "Linux", "version": "10.14.6"}},
    ]


@pytest.fixture
def mock_platform_list_2():
    """System and version doesn't match with the mocked one
    """
    return [
        {"name": "macos", "platform_info": {"system": "test1", "version": "test3"}},
        {"name": "ubuntu", "platform_info": {"system": "test2", "version": "test4"}},
    ]


def assert_ran_on_mac(system, version, mac_ver):
    """Run all the assertions if the test was ran on mac
    """
    system.assert_called_once()
    version.assert_called_once()
    mac_ver.assert_called_once()


def assert_ran_on_linux(system, version, mac_ver):
    """Run all the assertions if the test was ran on ubuntu
    """
    system.assert_called_once()
    version.assert_called_once()
    mac_ver.assert_not_called()


@pytest.mark.parametrize(
    "system, version, mac_ver, platform_list, platform_codename, assertion_fun",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list"),
            "test",
            assert_ran_on_mac,
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list"),
            "test",
            assert_ran_on_linux,
        ),
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list_2"),
            "test",
            assert_ran_on_mac,
        ),
    ],
)
def test_invalid_platform_codename(
    system, version, mac_ver, platform_list, platform_codename, assertion_fun
):
    """Testing if the `platform_codename` provided is valid or not
    """
    with pytest.raises(e.SpecificationError):
        _ = s.BlockPlatform(
            platform_codename=platform_codename, platform_list=platform_list
        )
        assertion_fun(system=system, version=version, mac_ver=mac_ver)


@pytest.mark.parametrize(
    "system, version, mac_ver, assertion_fun, expected_output",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            assert_ran_on_mac,
            {"system": "Darwin", "version": "10.10.10"},
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            assert_ran_on_linux,
            {"system": "Linux", "version": "10.14.6"},
        ),
    ],
)
def test_platform_info(system, version, mac_ver, assertion_fun, expected_output):
    """Testing if the current platform by the `BlockPlatform.current_platform` is accurate
    """
    obj = s.BlockPlatform()
    assertion_fun(system=system, version=version, mac_ver=mac_ver)
    assert obj.info == expected_output


class TestInitPlatform:
    """Testing the init for the Platform
    """

    @pytest.mark.parametrize(
        "system, version, mac_ver, platform_list, assertion_fun, expected_output",
        [
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                assert_ran_on_mac,
                "macos",
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                assert_ran_on_linux,
                "ubuntu",
            ),
        ],
    )
    def test_plat_list(
        self, system, version, mac_ver, platform_list, assertion_fun, expected_output
    ):
        """Testing if only passed the `platform_list`
        """
        obj = s.BlockPlatform(platform_list=platform_list)
        assertion_fun(system=system, version=version, mac_ver=mac_ver)
        assert obj.codename == expected_output

    @pytest.mark.parametrize(
        "system, version, mac_ver, platform_list, platform_codename, assertion_fun, expected_output",
        [
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "test",
                assert_ran_on_mac,
                "MOCK",
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "test",
                assert_ran_on_linux,
                "MOCK",
            ),
        ],
    )
    def test_plat_code(
        self,
        system,
        version,
        mac_ver,
        platform_list,
        platform_codename,
        assertion_fun,
        expected_output,
    ):
        """Testing if only passed the `platform_codename`
        """
        obj = s.BlockPlatform(platform_codename=platform_codename)
        assertion_fun(system=system, version=version, mac_ver=mac_ver)
        assert obj.codename == expected_output

    @pytest.mark.parametrize(
        "system, version, mac_ver, platform_list, platform_codename, assertion_fun, expected_output",
        [
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "macos",
                assert_ran_on_mac,
                "macos",
            ),
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "ubuntu",
                assert_ran_on_mac,
                "ubuntu",
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "ubuntu",
                assert_ran_on_linux,
                "ubuntu",
            ),
        ],
    )
    def test_plat_list_and_code(
        self,
        system,
        version,
        mac_ver,
        platform_list,
        platform_codename,
        assertion_fun,
        expected_output,
    ):
        """Testing if both `platform_code` and `platform_list` is passed
        """
        obj = s.BlockPlatform(
            platform_codename=platform_codename, platform_list=platform_list
        )
        assertion_fun(system=system, version=version, mac_ver=mac_ver)
        assert obj.codename == expected_output

    @pytest.mark.parametrize(
        "system, version, mac_ver, assertion_fun, expected_output",
        [
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                assert_ran_on_mac,
                "MOCK",
            ),
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                assert_ran_on_mac,
                "MOCK",
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                assert_ran_on_linux,
                "MOCK",
            ),
        ],
    )
    def test_no_args(self, system, version, mac_ver, assertion_fun, expected_output):
        """Testing if no argument is passed
        """
        obj = s.BlockPlatform()
        assertion_fun(system=system, version=version, mac_ver=mac_ver)
        assert obj.codename == expected_output


class TestPlatform:
    """Testing core functionalities of the Platform class
    """
