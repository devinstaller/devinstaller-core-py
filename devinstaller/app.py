"""The main module which is used by CLI and Library
"""
from typing import Any, Dict, List, Optional

import questionary
from typeguard import typechecked

from devinstaller import exceptions as e
from devinstaller import file_handler as f
from devinstaller import installer as i
from devinstaller import models as m
from devinstaller import schema as s


@typechecked
def install(
    file_path: Optional[str] = None,
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
    if file_path is not None:
        schema_object: Dict[Any, Any] = f.read(file_path)
    elif spec_object is not None:
        schema_object = spec_object
    else:
        raise e.DevinstallerError("Schema object not found", "D100")
    validated_schema_object: m.FullDocumentType = s.validate(schema_object)
    platform_object = s.get_platform_object(validated_schema_object, platform_codename)
    module_map = s.generate_module_map(
        validated_schema_object["modules"], platform_object
    )
    if requirements_list is None:
        requirement_list = ask_user_for_the_requirement_list(list(module_map.values()))
    i.main(module_map, requirement_list)


def ask_user_for_the_requirement_list(module_objects: List[m.Module]) -> List[str]:
    """Ask the user for which modules to be installed

    Args:
        module_objects: List of all the modules you want to display to the user

    Returns:
        List of the objects of all the modules to be installed.
    """
    print("Hey... You haven't selected which module to be installed")
    title = "Do you mind selected a few for me?"
    choices = {get_choice_text(m.display, m.description): m for m in module_objects}
    selections = questionary.checkbox(title, choices=list(choices.keys())).ask()
    data: List[str] = []
    for _s in selections:
        _m = choices[_s]
        data.append(_m.alias)
    return data


def get_choice_text(name: str, description: Optional[str]) -> str:
    """Returns the choice text for displaying to the user

    Args:
        name: Name of the module
        description: Optional description you want to print

    Returns:
        Text which is displayed to the user
    """
    if description is None:
        return f"{name}"
    return f"{name} - {description}"


def show(file_name: str) -> None:
    """TODO
    """
    # TODO Write the function to show all the modules defined in the spec file
