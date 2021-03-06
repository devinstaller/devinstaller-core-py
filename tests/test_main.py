from typing import Any, Dict, List, Optional, Set

from devinstaller_core import dependency_graph as dg
from devinstaller_core import lib

# from typeguard import typechecked


def get_req_list(dependency_graph: dg.DependencyGraph, requirements_list: List[str]):
    list_of_deps = list(dependency_graph.graph.keys())
    if len(list_of_deps) == 1:
        return list_of_deps
    elif requirements_list is not None:
        return requirements_list
    else:
        return lib.get_requirement_list(dependency_graph.module_list())


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
    dependency_graph: dg.DependencyGraph = lib.create_dependency_graph(
        schema_object=validated_schema_object, platform_codename=platform_codename
    )
    req_list = get_req_list(
        dependency_graph=dependency_graph, requirements_list=requirements_list
    )
    dependency_graph.install(req_list)
    orphan_modules_names = dependency_graph.orphan_modules
    if orphan_modules_names != set() and lib.get_user_confirmation(
        orphan_modules_names
    ):
        dependency_graph.uninstall_orphan_modules()


files = [
    # "file: tests/data/test.devfile.toml",
    # "file: tests/data/test.devfile.yaml",
    # "file: tests/data/test2.devfile.toml",
    "file: tests/data/test3.devfile.toml",
    # "file: tests/data/test4.devfile.toml",
    # "file: tests/data/test5.devfile.toml",
    # "file: tests/data/test6.devfile.toml"
    # "file: tests/data/test7.devfile.toml"
    # "file: tests/data/test8.devfile.toml"
]

for f in files:
    install(spec_file_path=f)
