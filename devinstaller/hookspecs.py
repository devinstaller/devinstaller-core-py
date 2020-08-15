import types
from typing import Any, Dict, List, Optional, Set

import pluggy

from devinstaller import models as m

hookspec = pluggy.HookspecMarker("devinstaller")

# pylint: disable=unused-argument


@hookspec
def create_dependency_graph(
    schema_object: m.TypeFullDocument, platform_codename: str
) -> m.ModuleDependency:
    """Create dependency graph
    """


@hookspec
def core(
    spec_file_path: Optional[str] = None, spec_object: Optional[Dict[Any, Any]] = None
) -> m.TypeFullDocument:
    """The core function.

    Validates and returns the schema object.
    """


@hookspec
def get_requirement_list(module_objects: List[m.TypeAnyModule],) -> List[str]:
    """Ask the user for which modules to be installed

    Args:
        module_objects: List of all the modules you want to display to the user

    Returns:
        List of the objects of all the modules to be installed.
    """


@hookspec
def get_user_confirmation(orphan_list: Set[str]) -> bool:
    """Asks user for confirmation for the uninstallation of the orphan modules.

    Args:
        orphan_list: The "list" of modules which are not used by any other modules
    """


@hookspec
def load_devfile(
    schema_object: m.TypeFullDocument, prog_file_path: Optional[str] = None
) -> types.ModuleType:
    """Loads the file and returns the module

    Args:
        schema_object: The full schema object
        prog_file_path: The path to the `prog_file`

    Returns:
        The module
    """


@hookspec
def download_devfile(file_path: str) -> str:
    """Downloads the devfile so that it can be loaded

    Args:
        file_path: The path to the file

    Returns:
        The path where the file is saved
    """


@hookspec
def load_python_module(
    file_path: str, module_name: str = "devfile"
) -> types.ModuleType:
    """Loads the module
    """


@hookspec
def get_platform_object(
    full_document: m.TypeFullDocument, platform_codename: Optional[str] = None
) -> m.PlatformBlock:
    """Create the platform object and return it
    """
