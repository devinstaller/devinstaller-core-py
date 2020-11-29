from typing import Any, Dict, List, Optional, Set

from typeguard import typechecked

from devinstaller_core import lib


def install(
    spec_file_path: Optional[str] = None,
    prog_file_path: Optional[str] = None,
    spec_object: Optional[Dict[Any, Any]] = None,
    platform_codename: Optional[str] = None,
    requirements_list: Optional[List[str]] = None,
) -> None:
    """Install the default preset and the modules which it requires.
    """
    validated_schema_object = lib.core(
        file_path=spec_file_path, spec_object=spec_object
    )
    dependency_graph = lib.create_dependency_graph(
        schema_object=validated_schema_object, platform_codename=platform_codename
    )
    req_list = (
        requirements_list
        if requirements_list is not None
        else lib.get_requirement_list(dependency_graph.module_list())
    )
    dependency_graph.install(req_list)
    orphan_modules_names = dependency_graph.orphan_modules
    if orphan_modules_names != set() and lib.get_user_confirmation(
        orphan_modules_names
    ):
        dependency_graph.uninstall_orphan_modules()


install(spec_file_path="file: tests/data/test.devfile.toml")
