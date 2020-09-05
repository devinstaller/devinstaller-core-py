import pytest

from devinstaller_core import dependency_graph as m
from devinstaller_core import exception as e


@pytest.fixture
def mock_modules_list():
    """Standard module list without any issues"""

    return [
        {"name": "foo", "module_type": "app", "supported_platforms": ["macos"]},
        {"name": "bar", "module_type": "app"},
    ]


@pytest.fixture
def mock_modules_list_2():
    """Module list where modules are sharing the same name"""
    return [
        {"name": "foo", "description": "First module", "module_type": "app"},
        {"name": "foo", "description": "First module", "module_type": "file"},
    ]


@pytest.fixture
def mock_modules_list_3():
    """Module list where module names are different but their alias are same"""
    return [
        {
            "name": "foo1",
            "alias": "foo",
            "description": "First module",
            "module_type": "app",
        },
        {
            "name": "foo2",
            "alias": "foo",
            "description": "First module",
            "module_type": "file",
        },
    ]


@pytest.fixture
def mock_modules_list_4():
    """Module list where module codename ends up being the same"""
    return [
        {"name": "foo", "description": "First module", "module_type": "app"},
        {
            "name": "foo1",
            "alias": "foo",
            "description": "First module",
            "module_type": "file",
        },
    ]


@pytest.fixture
def mock_modules_list_5():
    """Module list for testing dependency"""
    return [
        {
            "name": "foo",
            "module_type": "app",
            "install_inst": [{"cmd": "sh: echo 'hi'"}],
        }
    ]


@pytest.fixture
def mocked_user_input(mocker):
    """Mocking user input"""
    return mocker.patch("devinstaller_core.utilities.UserInteract.select")


@pytest.fixture
def mocked_user_input_first(mocked_user_input):
    """Mocking user input and return mock value"""
    mocked_user_input.return_value = "First one"
    return mocked_user_input


@pytest.fixture
def mocked_user_input_second(mocked_user_input):
    """Mocking user input and return mock value"""
    mocked_user_input.return_value = "Second one"
    return mocked_user_input


def get_platform_object(codename=None):
    obj = m.BlockPlatform()
    if codename is None:
        return obj
    obj.codename = codename
    return obj


@pytest.mark.parametrize(
    "platform_object, modules_list, expected_response",
    [
        (
            get_platform_object("macos"),
            pytest.lazy_fixture("mock_modules_list"),
            {"foo": m.ModuleApp(name="foo"), "bar": m.ModuleApp(name="bar")},
        ),
        (
            get_platform_object("test"),
            pytest.lazy_fixture("mock_modules_list"),
            {"bar": m.ModuleApp(name="bar")},
        ),
    ],
)
def test_graph_gen(platform_object, modules_list, expected_response):
    """Testing if the graph generated respects the platform codename"""
    module_map = m.DependencyGraph(
        module_list=modules_list, platform_object=platform_object
    )
    assert module_map.graph == expected_response


@pytest.mark.parametrize(
    "platform_object, modules_list, user_input",
    [
        (
            m.BlockPlatform(),
            pytest.lazy_fixture("mock_modules_list_2"),
            pytest.lazy_fixture("mocked_user_input_first"),
        ),
        (
            m.BlockPlatform(),
            pytest.lazy_fixture("mock_modules_list_2"),
            pytest.lazy_fixture("mocked_user_input_second"),
        ),
        (
            m.BlockPlatform(),
            pytest.lazy_fixture("mock_modules_list_3"),
            pytest.lazy_fixture("mocked_user_input_first"),
        ),
        (
            m.BlockPlatform(),
            pytest.lazy_fixture("mock_modules_list_4"),
            pytest.lazy_fixture("mocked_user_input_first"),
        ),
    ],
)
def test_duplicate_modules(platform_object, modules_list, user_input):
    """Testing if there are more than 1 module with same codename"""
    m.DependencyGraph(module_list=modules_list, platform_object=platform_object)
    user_input.assert_called_once()


@pytest.mark.parametrize(
    "platform_object, modules_list",
    [(get_platform_object(), pytest.lazy_fixture("mock_modules_list"))],
)
def test_platform_compatibility(platform_object, modules_list):
    """Testing if the platform compatibility error is raised

    If any of the modules has any information about the platform it can support in the
    form of `supported_platforms` then it will make sure it can safely validate the
    module compatibility.

    To make sure this it will check if the `platform_object` is not a "mock" object.

    The `BlockPlatform` returns a "mock" object if it can't find any info on the
    platforms.

    This "mock" object given by the `BlockPlatform` is in turn used for this.
    """
    with pytest.raises(e.SpecificationError):
        m.DependencyGraph(module_list=modules_list, platform_object=platform_object)


@pytest.mark.parametrize(
    "platform_object, modules_list, expected_response",
    [
        (get_platform_object("test"), pytest.lazy_fixture("mock_modules_list"), 1),
        (get_platform_object("macos"), pytest.lazy_fixture("mock_modules_list"), 2),
    ],
)
def test_module_list_method(platform_object, modules_list, expected_response):
    """Testing if the data returned by the `module_list`"""
    obj = m.DependencyGraph(module_list=modules_list, platform_object=platform_object)
    assert len(obj.module_list()) == expected_response


@pytest.mark.parametrize(
    "platform_object, module_list, requirement_list",
    [(get_platform_object(), pytest.lazy_fixture("mock_modules_list_5"), ["foo"])],
)
def test_graph_install(platform_object, module_list, requirement_list):
    obj = m.DependencyGraph(module_list=module_list, platform_object=platform_object)
    obj.install(requirement_list)
