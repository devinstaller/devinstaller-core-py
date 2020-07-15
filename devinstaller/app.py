from typing import List, Optional, Union

from typeguard import typechecked

from devinstaller import exceptions as e
from devinstaller import file_handler as f
from devinstaller import installer as i
from devinstaller import models as m
from devinstaller import schema as s


@typechecked
def install(
    schema_object: Union[str, m.FullDocumentType],
    platform_code_name: Optional[str] = None,
    group_name: Optional[str] = None,
    module_name: Optional[str] = None,
) -> None:
    """Install the default preset and the modules which it requires.
    For the regular command line usage the schema_object is the full file path
    but for usage from any python module you have the option of sending either
    the full file path or directly the schema object.

    If file path is given then the file is read and the object is loaded, but
    in either case the object will be validated before further processing.

    Args:
        schema_object: Takes in either a file path or the document object
        platform_code_name: The name of the platform
        group: The name of the group of modules to be installed
        module: The name of the module to installed
    """
    if isinstance(schema_object, str):
        schema_object = f.read(schema_object)
    validated_schema_object = s.validate(schema_object)
    platform_object = s.get_platform_object(validated_schema_object, platform_code_name)
    dependency_graph = s.generate_dependency(validated_schema_object, platform_object)
    if module_name is not None:
        requirement_list = [module_name]
    if group_name is not None:
        requirement_list = get_requirements_list(
            validated_schema_object, group_name, 102
        )
    else:
        try:
            requirement_list = get_requirements_list(
                validated_schema_object, platform_object["default"], 102
            )
        except KeyError:
            raise e.SchemaComplianceError(
                errors=f"I couldn't find the key: `default` inside {platform_object['name']}"
            )
    i.main(dependency_graph, requirement_list)


def get_requirements_list(
    schema_object: m.FullDocumentType, group_name: str, error_code: int
) -> List[str]:
    """Returns the list of module code names which is to be installed

    Args:
        schema_object: The full validated schema document
        group_name: The name of the group
        error_code: The error to be raised if the group_name doesn't matches with the groups declared in the spec

    Returns:
        List of the module names to be installed
    """
    for _group in schema_object["groups"]:
        if _group["name"] == group_name:
            return _group["requires"]
    raise e.RuleViolationError(error_code)


def show(file_name: str) -> None:
    """Show all the groups and modules available for your OS.
    """
    # TODO
    file_path = file_name
    full_document = s.validate(f.read(file_path))
    pass
