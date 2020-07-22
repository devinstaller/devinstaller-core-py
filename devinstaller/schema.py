# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Wed 22 Jul 2020 17:17:52 IST
#
# schema.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description:
#
# Copyright (c) 2020, Justine Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the

# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------

"""Handles everything related to spec file schema"""
import platform
from typing import Any, Dict, List, Optional, Union, cast

import cerberus
import questionary
from typeguard import typechecked

# from devinstaller import commands as c
from devinstaller import exceptions as e
from devinstaller import models as m

DEVFILE_SCHEMA = m.schema()


@typechecked
def validate(
    document: Dict[Any, Any], schema: Dict[Any, Any] = DEVFILE_SCHEMA
) -> m.ValidateResponseType:
    """Validate the given document with the schema

    Args:
        document: Python object which has to be validated
        schema: It can also take in custom schema for validation. Default is the Full file schema

    Returns:
        A dict with its validity, document and its errors.
    """
    _v = cerberus.Validator(schema)
    data: m.ValidateResponseType = {
        "valid": _v.validate(document),
        "document": _v.document,
        "errors": _v.errors,
    }
    return data


@typechecked
def get_validated_document(
    document: Dict[Any, Any], schema: Dict[Any, Any] = m.schema()
) -> m.FullDocumentType:
    """Validate the given document with the schema

    Args:
        document: Python object which has to be validated
        schema: It can also take in custom schema for validation. Default is the Full file schema

    Returns:
        Validated object

    Raises:
        SpecificationError
            with error code :ref:`error-code-100`
    """
    data = validate(document)
    if data["valid"]:
        return cast(m.FullDocumentType, data["document"])
    raise e.SpecificationError(str(data["errors"]), "S100")


@typechecked
def remove_key_from_dict(input_dictionary: Dict[Any, Any], key: str) -> Dict[Any, Any]:
    """Remove the key and its value from the dictionary

    The original dictionary is not modified instead a copy is made and modified and that is returned.

    Args:
        input_dictionary: Any dictionary
        key: The key and its value you want to remove

    Returns:
        A new dictionary without the specified key
    """
    if key not in input_dictionary:
        return input_dictionary
    new_dictionary = input_dictionary.copy()
    new_dictionary.pop(key)
    return new_dictionary


@typechecked
def generate_module_map(
    modules_list: List[m.ModuleType], platform_object: m.PlatformType
) -> m.ModuleMapType:
    """Generate `module_map` object from the data.
    The `module_map` houses all the modules and their dependency on each other

    Args:
        modules_list: List of all modules
        platform_object: Plaform object of the current platform

    Returns:
        The `module_map` object for that specific platform
    """
    response: m.ModuleMapType = {}
    for module_object in modules_list:
        if check_for_module_platform_compatibility(platform_object, module_object):
            assert "name" in module_object
            codename: str = module_object.get("alias", module_object["name"])
            module_object["alias"] = codename
            new_module = create_module(module_object)
            if codename in response:
                response[codename] = ask_user_for_which_module(
                    old_module=response[codename], new_module=new_module
                )
            else:
                response[codename] = new_module
    return response


@typechecked
def create_module(module_object: m.ModuleType) -> m.Module:
    """Creates the module object for the `module_map` using the module dict.

    Note: The `Module` class needs `alias` to init. In normal execution flow this is already handled
    before calling this function. If it is not in its normal execution flow this should be handled by
    the function calling this.

    Args:
        module_object: The module object which needs to serialized into a `Module` class object

    Returns:
        `Module` class object

    Raises:
        AssertionError
            if the requirements of the input data is not matched
    """
    assert "name" in module_object
    temp_obj: Dict[str, Any] = dict(**module_object)
    temp_obj = remove_key_from_dict(temp_obj, "supported_platforms")
    temp_obj["display"] = module_object.get("display", module_object["name"])
    temp_obj["init"] = create_install_steps(module_object, step_name="init")
    temp_obj["config"] = create_install_steps(module_object, step_name="config")
    temp_obj["command"] = create_install_steps(module_object, step_name="command")
    assert "name" in temp_obj
    assert "alias" in temp_obj
    assert "module_type" in temp_obj
    assert "display" in temp_obj
    return m.Module(**temp_obj)


@typechecked
def create_install_steps(
    module_object: m.ModuleType, step_name: str
) -> Union[List[m.ModuleInstallInstruction], m.ModuleInstallInstruction, None]:
    """Creates either an object or a list of objects of class `ModuleInstallInstruction`.

    This is done before serializing the `Module` object.
    The `Module` class needs the installation steps for the module as objects of `ModuleInstallInstructions`.

    Args:
        module_object: The object whose installation steps needs to be serialized into objects
        step_name: The name of the step which will be serialized

    Returns:
        Either a object or a list of `ModuleInstallInstruction` objects
    """
    if step_name in module_object:
        if isinstance(module_object[step_name], list):
            return [
                create_module_install_instruction(i) for i in module_object[step_name]
            ]
        return create_module_install_instruction(module_object[step_name])
    return None


@typechecked
def create_module_install_instruction(
    instruction: Union[str, m.ModuleInstallInstructionType]
) -> m.ModuleInstallInstruction:
    """Creates the module instruction object for the module

    The instruction can be either a string which is assumed to be the installation instruction or
    it can be a dict with the installation and its rollback instructions

    Args:
        instruction: The instruction to be serialized

    Returns:
        The instruction as a object of `ModuleInstallInstruction` class
    """
    if isinstance(instruction, str):
        return m.ModuleInstallInstruction(instruction)
    return m.ModuleInstallInstruction(**instruction)


@typechecked
def ask_user_for_which_module(old_module: m.Module, new_module: m.Module) -> m.Module:
    """Sometimes the spec may have already declared two modules with same codename and for the same platform

    In such cases we ask the user to select which one to use for the current session.

    Only one can be used for the current session.

    Please note that the spec allows for multiple modules with same codename and usually they are for different platforms
    but other wise you need to select one. You can't use multiple modules with same codename in the same session.

    Args:
        old_module: The old module which is already present in the `module_map`
        new_module: The new module which happens to share the same codename of the `old_module`

    Returns:
        The selected module
    """
    print("Oops, looks like your spec has two modules with the same codename.")
    print("But for the current session I can use only one.")
    print("This is the first module")
    print(old_module)
    print("And this is the second module")
    print(new_module)
    title = "Do you mind selecting one?"
    choices = ["First one", "Second one"]
    selection = questionary.select(title, choices=choices).ask()
    if selection == "First one":
        return old_module
    return new_module


@typechecked
def check_for_module_platform_compatibility(
    platform_object: m.PlatformType, module: m.ModuleType
) -> bool:
    """Checks if the given module is compatible with the current platform.

    Steps:
        1. Checks if the user has provided `supported_platforms` key-value pair
           in the module object. If it is NOT provided then it is assumed that this specific
           module is compatible with all platforms and returns True.
        2. Checks if the platform object is a "mock" platform object or not.
           If the user didn't provided platforms block in the spec a "mock"
           platform object as placeholder is generated. So it checks whether is
           this the mock object or not. If it is then `SpecificationError` is raised.
        3. Checks if the platform name is supported by the module. If yes then returns True.
        4. Nothing else then returns False

    Args:
        platform_object: The current platform object
        module: The module object

    Returns:
        True if compatible else False

    Raises:
        SpecificationError
            with error code :ref:`error-code-100`
    """
    if "supported_platforms" not in module:
        return True
    if platform_object["name"] == "MOCK":
        raise e.SpecificationError(
            module["name"], "S100", "You are missing a platform object"
        )
    if platform_object["name"] in module["supported_platforms"]:
        return True
    return False


@typechecked
def get_platform_object(
    full_document: m.FullDocumentType, platform_code_name: Optional[str] = None
) -> m.PlatformType:
    """Main function to get the platform object.

    Steps:
        1. If `platform_code_name` is provided then that is used to get the platform object
        2. If not present then current platform is checked against all the platforms defined

    Args:
        full_document: The full spec file
        platform_code_name: name of the platform

    Returns:
        The platform object
    """
    if not platform_code_name:
        if "platforms" in full_document:
            current_platform = get_current_platform()
            platform_list = full_document["platforms"]
            return get_platform_object_using_system(platform_list, current_platform)
        return get_mock_platform_object()
    return get_platform_object_from_codename(
        full_document["platforms"], platform_code_name
    )


@typechecked
def get_mock_platform_object() -> m.PlatformType:
    """Returns a mock platform object

    Returns:
        Mock platform object
    """
    return {
        "name": "MOCK",
        "description": "MOCK",
        "platform_info": {"system": "MOCK", "version": "MOCK"},
    }


@typechecked
def get_platform_object_from_codename(
    platform_list: List[m.PlatformType], platform_codename: str
) -> m.PlatformType:
    """Returns the platform object whose name matches the `platform_codename`.

    Args:
        full_document: The full spec file
        platform_codename: name of the platform

    Raises:
        SpecificationError
            with error code :ref:`error-code-S100`
    """
    for _plat in platform_list:
        if _plat["name"] == platform_codename:
            return _plat
    raise e.SpecificationError(platform_codename, "S100", "You are missing a platform")


@typechecked
def get_platform_object_using_system(
    platform_list: List[m.PlatformType], current_platform: m.PlatformInfoType
) -> m.PlatformType:
    """Gets the current platform code name

    Args:
        platform_list: List of all platforms declared in the spec
        current_platform: The current platform object

    Returns:
        The `code_name` of current platform
    """
    platforms_supported: List[m.PlatformType] = []
    for _p in platform_list:
        if compare_strings(_p["platform_info"]["system"], current_platform["system"]):
            if "version" not in _p["platform_info"]:
                platforms_supported.append(_p)
            elif compare_version(
                current_platform["version"], _p["platform_info"]["version"]
            ):
                platforms_supported.append(_p)
    if len(platforms_supported) == 1:
        print(f"I see you are using {platforms_supported[0]['name']}")
        return platforms_supported[0]
    return ask_user_for_platform_object(platforms_supported)


@typechecked
def ask_user_for_platform_object(
    platforms_supported: List[m.PlatformType],
) -> m.PlatformType:
    """Ask the user for which platform to be used.

    Sometimes it may happen that platform code name is not provided by the user so the
    system tries to figure which platform it is currently running.

    But it may happen that multiple platforms defined satisfy the conditions, in that case
    we will explicitly ask the user to select one of the platforms which are satisfied.

    Args:
        platforms_supported: List of platform objects which satisfies the condition

    Returns:
        The required platform object
    """
    print(
        'Hey.. your current platform supports multiple "platform" declared in the spec file'
    )
    title = "Do you mind narrowring it down to one for me?"
    choices = [p["name"] for p in platforms_supported]
    selection = questionary.select(title, choices=choices).ask()
    return get_platform_object_from_codename(platforms_supported, selection)


@typechecked
def compare_version(version: str, expected_version: str) -> bool:
    """Compares the version of the current platform and the version info in the spec file.

    TODO Works with both the platforms block and the modules block?

    Uses the semver specification to compare.
    """
    # TODO How to compare using the semver specification.
    # TODO What about the modules which doesnt' use the semver spec?
    if version == expected_version:
        return True
    return False


@typechecked
def compare_strings(*args: str) -> bool:
    """Compare all the strings with each other (case insensitive)

    Args:
        Any number of string arguments.
        At least one argument required else it will return False.
        If one argument then it will return True.

    Returns:
        True if all matches else False
    """
    if len({v.casefold() for v in args}) != 1:
        return False
    return True


@typechecked
def get_current_platform() -> m.PlatformInfoType:
    """Get the current platform object

    Returns:
        The current platform object
    """
    data: m.PlatformInfoType = {
        "system": platform.system(),
        "version": platform.version(),
    }
    if data["system"] == "Darwin":
        data["version"] = platform.mac_ver()[0]
    return data
