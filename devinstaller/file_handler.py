# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:40:37 IST
# Last-Updated: Tue 21 Jul 2020 21:09:11 IST
#
# file_handler.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles everything file related
#
# Copyright (c) 2020, Justin Kizhakkinedath
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

"""Handles everything file_handler"""
import hashlib
import os
import re
from typing import Any, Dict

import anymarkup
from typeguard import typechecked

from devinstaller import exceptions as e


@typechecked
def parse_contents(file_contents: str, file_format: str = "toml") -> Dict[Any, Any]:
    """Parse `file_contents` and returns the python object

    Args:
        file_contents: The contents of file

    Returns:
        Python object

    Raises:
        SpecificationError
            with code :ref:`error-code-S100`
    """
    try:
        return anymarkup.parse(file_contents, format=file_format)
    except Exception:
        raise e.SpecificationError(
            error=file_contents,
            error_code="S100",
            message="There is some error in your file content",
        )


@typechecked
def read_file(file_path: str) -> str:
    """Reads the file at the path and returns the string representation

    Args:
        file_path: The path to the file

    Returns:
        String representation of the file
    """
    # TODO check if the path is starting with dot or two dots
    full_path = os.path.expanduser(file_path)
    with open(full_path, "r") as f:
        return f.read()


@typechecked
def read_file_and_parse(file_path: str) -> Dict[Any, Any]:
    """Reads the file at path and parse and returns the python object

    It is composed of `read_file` and `parse_contents`

    Args:
        file_path: The path to the file

    Returns:
        Python object
    """
    file_format = file_path.split(".")[-1]
    return parse_contents(read_file(file_path), file_format=file_format)


@typechecked
def download(url: str) -> Dict[Any, Any]:
    """Downloads file from the internet

    Args:
        url: Url of the file

    Returns:
        Python object
    """
    # TODO


@typechecked
def check_and_download(file_path: str) -> Dict[Any, Any]:
    """Checks the input_str and downloads or reads the file.

    Steps:
        1. Extract the method: `file` or `url`
        2. If file then expand the file path and stores it for checking dependency cycle and downloads the file
        3. If url the stores the it for checking the dependency cycle
        4. Either way reads the file and returns the object.

    Args:
        file_path: path to file. Follows the spec format

    Returns:
        Python dict

    Raises:
        SpecificationError
            with error code :ref:`error-code-S101`
    """

    try:
        pattern = r"^(url|file): (.*)"
        result = re.match(pattern, file_path)
        assert result is not None
        method = result.group(1)
        file_path = result.group(2)
        function = {"file": read_file_and_parse, "url": download}
        file_contents = function[method](file_path)
        data = {"digest": hash(str(file_contents)), "contents": file_contents}
        return data
    except AssertionError:
        raise e.SpecificationError(
            error=file_path,
            error_code="S101",
            message="The file_path you gave didn't start with `url: ` or `file: `.",
        )


@typechecked
def hash(input_data: str) -> str:
    """Hashes the input string and returns its digest
    """
    return hashlib.sha256(input_data.encode("utf-8")).hexdigest()
