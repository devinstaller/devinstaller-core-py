import pytest

from devinstaller_core import block_platform as s
from devinstaller_core import exception as e

MOCKED_PLATFORM_CODE = "MOCK"
EXPECTED_MAC_PLATFORM_INFO = {"system": "Darwin", "version": "10.10.10"}
EXPECTED_LINUX_PLATFORM_INFO = {"system": "Linux", "version": "10.14.6"}


@pytest.fixture
def mocked_system(mocker):
    """Mocking `plaform.system`
    """
    return mocker.patch("platform.system")


@pytest.fixture
def mocked_version(mocker):
    """Mocking `plaform.version`
    """
    return mocker.patch("platform.version")


@pytest.fixture
def mocked_mac_ver(mocker):
    """Mocking `plaform.mac_ver`

    On MacOS to get the version you need `platform.mac_ver` and this is mocked
    for testing
    """
    mock = mocker.patch("platform.mac_ver")
    mock.return_value = ("10.10.10", ("", "", ""), "x86_64")
    return mock


@pytest.fixture
def mocked_user_input(mocker):
    """Mocking user input
    """
    return mocker.patch("devinstaller_core.utilities.UserInteract.select")


@pytest.fixture
def mocked_user_input_dummy(mocked_user_input):
    """Mocking user input and return mock value
    """
    mocked_user_input.return_value = MOCKED_PLATFORM_CODE
    return mocked_user_input


@pytest.fixture
def mocked_user_input_macos(mocked_user_input):
    """Mocking user input and return `macos`
    """
    mocked_user_input.return_value = "macos"
    return mocked_user_input


@pytest.fixture
def mocked_user_input_linux(mocked_user_input):
    """Mocking user input and return `macos`
    """
    mocked_user_input.return_value = "linux"
    return mocked_user_input


@pytest.fixture
def mocked_system_mac(mocked_system):
    """This fixture takes in the `mocked_system` and sets a return value which
    says that the system detected is a mac.
    """
    mocked_system.return_value = "Darwin"
    return mocked_system


@pytest.fixture
def mocked_system_linux(mocked_system):
    """This fixture takes in the `mocked_system` and sets a return value which
    says that the system detected is a linux machine.
    """
    mocked_system.return_value = "Linux"
    return mocked_system


@pytest.fixture
def mocked_version_dummy(mocked_version):
    """This fixture takes in the `mocked_version` and sets a return value which
    says that the version of the detected operating system is some dummy value.
    """
    mocked_version.return_value = "test"
    return mocked_version


@pytest.fixture
def mocked_version_linux(mocked_version):
    """This fixture takes in the `mocked_version` and sets a return value which
    says that the version of the detected operating system is specific to linux OS.
    """
    mocked_version.return_value = "10.14.6"
    return mocked_version


@pytest.fixture
def mock_platform_list():
    """Standard platform list. This list doesn't have any issues and conforms to the spec.
    """
    data = [
        {"name": "macos", "platform_info": EXPECTED_MAC_PLATFORM_INFO},
        {"name": "ubuntu", "platform_info": EXPECTED_LINUX_PLATFORM_INFO},
    ]
    return data


@pytest.fixture
def mock_platform_list_2():
    """System and version doesn't match with the mocked one
    """
    return [
        {"name": "macos", "platform_info": {"system": "test1", "version": "test3"}},
        {"name": "ubuntu", "platform_info": {"system": "test2", "version": "test4"}},
    ]


@pytest.fixture
def mock_platform_list_3():
    """System and version doesn't match with the mocked one
    """
    return [
        {"name": "macos", "platform_info": {"system": "test1", "version": "test3"}},
        {"name": "macos", "platform_info": {"system": "test1.1", "version": "test3.1"}},
        {"name": "ubuntu", "platform_info": {"system": "test2", "version": "test4"}},
    ]


@pytest.fixture
def mock_platform_list_4():
    """Platform list where multiple platforms defined matches
    """
    return [
        {"name": "macos", "platform_info": EXPECTED_MAC_PLATFORM_INFO},
        {"name": "macos2", "platform_info": EXPECTED_MAC_PLATFORM_INFO},
        {"name": "ubuntu", "platform_info": EXPECTED_LINUX_PLATFORM_INFO},
        {"name": "ubuntu2", "platform_info": EXPECTED_LINUX_PLATFORM_INFO},
    ]


@pytest.fixture
def mock_platform_list_5():
    """Partial enty in the `platform_info` as well as version fail
    """
    return [
        {
            "name": "macos1",
            "platform_info": {
                "system": EXPECTED_MAC_PLATFORM_INFO["system"],
                "version": "test",
            },
        },
        {
            "name": "macos2",
            "platform_info": {"system": EXPECTED_MAC_PLATFORM_INFO["system"]},
        },
        {
            "name": "linux1",
            "platform_info": {
                "system": EXPECTED_LINUX_PLATFORM_INFO["system"],
                "version": "test",
            },
        },
        {
            "name": "linux2",
            "platform_info": {"system": EXPECTED_LINUX_PLATFORM_INFO["system"]},
        },
    ]


def assert_ran_on_mac(system, version, mac_ver):
    """Run all the assertions if the test was ran on mac
    """
    system.assert_called_once()
    version.assert_called_once()
    mac_ver.assert_called_once()


def assert_ran_on_mac_2(system, version, mac_ver, user_input):
    """Run all the assertions if the test was ran on mac as well as it used the
    `BlockPlatform.resolve` method to resolve ambiguious platform selection
    """
    assert_ran_on_mac(system=system, version=version, mac_ver=mac_ver)
    user_input.assert_called_once()


def assert_ran_on_linux(system, version, mac_ver):
    """Run all the assertions if the test was ran on ubuntu
    """
    system.assert_called_once()
    version.assert_called_once()
    mac_ver.assert_not_called()


def assert_ran_on_linux_2(system, version, mac_ver, user_input):
    """Run all the assertions if the test was ran on ubuntu
    """
    assert_ran_on_linux(system=system, version=version, mac_ver=mac_ver)
    user_input.assert_called_once()


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
    "system, version, mac_ver, platform_list, platform_codename, assertion_fun",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list_3"),
            "macos",
            assert_ran_on_mac,
        )
    ],
)
def test_duplicate_platforms(
    system, version, mac_ver, platform_list, platform_codename, assertion_fun
):
    """Testing if there is more than one platform with the same codename
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
            EXPECTED_MAC_PLATFORM_INFO,
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            assert_ran_on_linux,
            EXPECTED_LINUX_PLATFORM_INFO,
        ),
    ],
)
def test_platform_info(system, version, mac_ver, assertion_fun, expected_output):
    """Testing if the current platform by the `BlockPlatform.current_platform` is accurate
    """
    obj = s.BlockPlatform()
    assertion_fun(system=system, version=version, mac_ver=mac_ver)
    assert obj.info == expected_output


@pytest.mark.parametrize(
    "system, version, mac_ver, user_input, platform_list, assertion_fun, expected_response",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mocked_user_input_macos"),
            pytest.lazy_fixture("mock_platform_list_4"),
            assert_ran_on_mac_2,
            "macos",
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mocked_user_input_linux"),
            pytest.lazy_fixture("mock_platform_list_4"),
            assert_ran_on_linux_2,
            "linux",
        ),
    ],
)
def test_multiple_selected(
    system,
    version,
    mac_ver,
    user_input,
    platform_list,
    assertion_fun,
    expected_response,
):
    """Testing if multiple platforms defined in the spec are satisfying the conditions
    """
    obj = s.BlockPlatform(platform_list=platform_list)
    assertion_fun(
        system=system, version=version, mac_ver=mac_ver, user_input=user_input
    )
    assert obj.codename == expected_response


@pytest.mark.parametrize(
    "system, version, mac_ver, platform_list, assertion_fun, expected_response",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list_5"),
            assert_ran_on_mac,
            "macos2",
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mock_platform_list_5"),
            assert_ran_on_linux,
            "linux2",
        ),
    ],
)
def test_partial_platform_info(
    system, version, mac_ver, platform_list, assertion_fun, expected_response
):
    """Testing if only the `system` attribute is provided as well as `version` failing.

    In the `platform_info` only the `system` attribute is mandatory, the `version` is not.

    Testing if the version doesn't satisfy the required conditions.

    The `version` attribute lets us drill down if the detected OS is satisfing
    the required conditions.

    This will test if only the `system` attribute satisfies but the `version` attribute
    fails.
    """
    obj = s.BlockPlatform(platform_list=platform_list)
    assertion_fun(system=system, version=version, mac_ver=mac_ver)
    assert obj.codename == expected_response


@pytest.mark.parametrize(
    "system, version, mac_ver, user_input, platform_list, assertion_fun, expected_response",
    [
        (
            pytest.lazy_fixture("mocked_system_mac"),
            pytest.lazy_fixture("mocked_version_dummy"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mocked_user_input_macos"),
            pytest.lazy_fixture("mock_platform_list_2"),
            assert_ran_on_mac_2,
            "macos",
        ),
        (
            pytest.lazy_fixture("mocked_system_linux"),
            pytest.lazy_fixture("mocked_version_linux"),
            pytest.lazy_fixture("mocked_mac_ver"),
            pytest.lazy_fixture("mocked_user_input_linux"),
            pytest.lazy_fixture("mock_platform_list_2"),
            assert_ran_on_linux_2,
            "linux",
        ),
    ],
)
def test_none_selected(
    system,
    version,
    mac_ver,
    user_input,
    platform_list,
    assertion_fun,
    expected_response,
):
    """Testing if no platforms defined in the spec file is satisfying the condition
    """
    obj = s.BlockPlatform(platform_list=platform_list)
    assertion_fun(
        system=system, version=version, mac_ver=mac_ver, user_input=user_input
    )
    assert obj.codename == expected_response


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
                MOCKED_PLATFORM_CODE,
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                pytest.lazy_fixture("mock_platform_list"),
                "test",
                assert_ran_on_linux,
                MOCKED_PLATFORM_CODE,
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
                MOCKED_PLATFORM_CODE,
            ),
            (
                pytest.lazy_fixture("mocked_system_mac"),
                pytest.lazy_fixture("mocked_version_dummy"),
                pytest.lazy_fixture("mocked_mac_ver"),
                assert_ran_on_mac,
                MOCKED_PLATFORM_CODE,
            ),
            (
                pytest.lazy_fixture("mocked_system_linux"),
                pytest.lazy_fixture("mocked_version_linux"),
                pytest.lazy_fixture("mocked_mac_ver"),
                assert_ran_on_linux,
                MOCKED_PLATFORM_CODE,
            ),
        ],
    )
    def test_no_args(self, system, version, mac_ver, assertion_fun, expected_output):
        """Testing if no argument is passed
        """
        obj = s.BlockPlatform()
        assertion_fun(system=system, version=version, mac_ver=mac_ver)
        assert obj.codename == expected_output
