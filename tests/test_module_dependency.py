import pytest

from devinstaller_core import dependency_graph as m


@pytest.fixture
def modules_list():
    return [
        {"name": "foo", "module_type": "app", "supported_platforms": ["macos"]},
        {"name": "bar", "module_type": "app"},
    ]


class TestGenerateModuleMap:
    def test_1(self, modules_list):
        """Testing if both foo and bar modules are returned.
        foo is explicity supported and bar is implicitly.
        """
        platform_object = m.BlockPlatform()
        platform_object.codename = "macos"
        module_map = m.ModuleDependency(modules_list, platform_object)
        expected_response = {
            "foo": m.ModuleApp(name="foo"),
            "bar": m.ModuleApp(name="bar"),
        }
        assert module_map.graph == expected_response

    def test_2(self, modules_list):
        """Testing if only bar module is returned.
        foo is NOT supported and bar is supported implicitly.

        Here the platform is `test` and it is explicitly not supported by foo,
        but it is implicitly supported by bar.
        """
        platform_object = m.BlockPlatform()
        platform_object.codename = "test"
        module_map = m.ModuleDependency(modules_list, platform_object)
        expected_response = {"bar": m.ModuleApp(name="bar")}
        assert module_map.graph == expected_response
