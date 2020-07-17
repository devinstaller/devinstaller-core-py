"""The main module which is used by CLI
"""
from typing import List, Optional, Union

import click
import pick
from typeguard import typechecked

from devinstaller import exceptions as e
from devinstaller import file_handler as f
from devinstaller import installer as i
from devinstaller import models as m
from devinstaller import schema as s


@typechecked
def install(
    file_path: Optional[str] = None,
    spec_object: Optional[dict] = None,
    platform_codename: Optional[str] = None,
    module_name: Optional[str] = None,
) -> None:
    """Install the default preset and the modules which it requires.
    There are two ways this function works.
    1. Passing the file_path (Default method for the CLI usage)
    2. Passing the spec_object

    If you pass the file path then it takes the precedance and the file is read
    and the object is loaded.
    If not then it checks for the schema_object and if it is not present then
    RuleVioloationError 105 is raised.

    And in either case the object will be validated before further processing.

    Args:
        file_path: Takes in path to the spec file
        spec_object: Takes in the full spec file as a python dict
        platform_codename: The name of the platform
        module: The name of the module to installed
    """
    if file_path is not None:
        schema_object: dict = f.read(file_path)
    elif spec_object is not None:
        schema_object = spec_object
    else:
        raise e.RuleViolationError(105)
    validated_schema_object: m.FullDocumentType = s.validate(schema_object)
    platform_object = s.get_platform_object(validated_schema_object, platform_codename)
    dependency_graph = s.generate_dependency(validated_schema_object, platform_object)
    if module_name is None:
        requirement_list = ask_user_for_the_requirement_list(
            list(dependency_graph.values())
        )
    else:
        requirement_list = [module_name]
    i.main(dependency_graph, requirement_list)


def ask_user_for_the_requirement_list(module_objects: List[m.Module]) -> List[str]:
    """Ask the user for which modules to be installed

    Args:
        module_objects: List of all the modules you want to display to the user

    Returns:
        List of the objects of all the modules to be installed.
    """
    print("Hey... You haven't selected which module to be installed")
    title = "Do you mind selected a few for me?"
    options = [m.display for m in module_objects]
    selections = pick.pick(options, title, multiselect=True, min_selection_count=1)
    data = []
    for _s in selections:
        _m = module_objects[_s[1]]
        data.append(_m.codename)
    return data


def show(file_name):
    """TODO
    """
    # TODO Write the function to show all the modules defined in the spec file
