from typing import Any, Dict, List, Optional, Set

import pluggy
from typeguard import typechecked

from devinstaller import hookspecs, lib
from devinstaller import models as m


def get_plugin_manager():
    pm = pluggy.PluginManager("devinstaller")
    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints("devinstaller")
    pm.register(lib)
    return pm


class Devinstaller:
    def __init__(self):
        pm = get_plugin_manager()
        self.hook = pm.hook

    @typechecked
    def install(
        self,
        spec_file_path: Optional[str] = None,
        prog_file_path: Optional[str] = None,
        spec_object: Optional[Dict[Any, Any]] = None,
        platform_codename: Optional[str] = None,
        requirements_list: Optional[List[str]] = None,
    ) -> None:
        """Install the default preset and the modules which it requires.

        There are two ways this function works.

        1. Passing the file_path (Default method for the CLI usage)
        2. Passing the spec_object

        If you pass the file path then it takes the precedance and the file is read
        and the object is loaded.

        If not then it checks for the schema_object and if it is not present then
        `ImplementationError` is raised.

        And in either case the object will be validated before further processing.

        Args:
            file_path: Takes in path to the spec file
            spec_object: Takes in the full spec file as a python dict
            platform_codename: The name of the platform
            module: The name of the module to installed

        raises:
            ImplementationError
                with error code :ref:`error-code-D100`
        """
        validated_schema_object = self.hook.core(
            spec_file_path=spec_file_path, spec_object=spec_object
        )
        dependency_graph = self.hook.create_dependency_graph(
            schema_object=validated_schema_object, platform_codename=platform_codename
        )
        if requirements_list is None:
            requirement_list = self.hook.get_requirement_list(
                dependency_graph.module_list()
            )
        dependency_graph.install(requirement_list)
        orphan_modules_names = dependency_graph.orphan_modules
        if orphan_modules_names != set():
            if self.hook.get_user_confirmation(orphan_modules_names):
                dependency_graph.uninstall_orphan_modules()
        return None

    @typechecked
    def show(self, file_name: str) -> None:
        """TODO Write the function to show all the modules defined in the spec file
        """

    @typechecked
    def run(
        self,
        interface_name: Optional[str] = None,
        spec_file_path: Optional[str] = None,
        prog_file_path: Optional[str] = None,
        spec_object: Optional[Dict[Any, Any]] = None,
        platform_codename: Optional[str] = None,
    ) -> m.TypeFullDocument:
        """The `run` function.

        This function is used for the interface block.
        """
        schema_object = self.hook.core(spec_file_path, spec_object)
        dev_module = self.hook.load_devfile(
            schema_object=schema_object, prog_file_path=prog_file_path
        )
        interface = m.get_interface(
            interface_list=schema_object["interfaces"], interface_name=interface_name
        )
        dependency_graph = self.hook.create_dependency_graph(
            schema_object=schema_object, platform_codename=platform_codename
        )
