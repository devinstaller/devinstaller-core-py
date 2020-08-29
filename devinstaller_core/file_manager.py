# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:40:37 IST
# Last-Updated: Sun 23 Aug 2020 00:02:43 IST
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
from dataclasses import dataclass
from typing import Any, Callable, Dict

import anymarkup
import requests
from typeguard import typechecked

from devinstaller_core import exception as e


class FileManager:
    """The class containing the methods require to handle files
    """

    @classmethod
    def read(cls, file_path: str) -> str:
        """Reads the file at the path and returns the string representation

        Args:
            file_path: The path to the file

        Returns:
            String representation of the file
        """
        # TODO check if the path is starting with dot or two dots
        full_path = os.path.expanduser(file_path)
        with open(full_path, "r") as _f:
            return _f.read()

    @classmethod
    def download(cls, url: str) -> str:
        """Downloads file from the internet

        Args:
            url: Url of the file

        Returns:
            String representation of file
        """
        response = requests.get(url)
        return response.content.decode("utf-8")

    @classmethod
    def save(cls, file_content: str, file_path: str) -> None:
        """Downloads file from the internet and saves to file
        """
        with open(file_path, "w") as f:
            f.write(file_content)

    @classmethod
    def hash_data(cls, input_data: str) -> str:
        """Hashes the input string and returns its digest
        """
        return hashlib.sha256(input_data.encode("utf-8")).hexdigest()


class DevFile:
    """Handles everything related to the `devfile`.

    Data attributes:
        digest: Contains the SHA-256 hash of the contents
        contents: The Spec file Python object

    Class attributes:
        pattern: This is the regex pattern used to parse the input path
        f_m: This is the object containing the file manager session
        hash_method: This method is used to hash the data
        extract: This is a dict with all the methods that is used to extract the data
    """

    @typechecked
    def __init__(self, file_path: str) -> None:
        """Checks the input_str and downloads or reads the file.

        Methods:
            url:
                downloads the file
            file:
                reads the file
            data:
                returns the data as is

        Steps:
            1. Extract the method
            2. Use the method to get the file
            3. hash the contents and returns the response object

        Args:
            file_path: path to file. Follows the spec format

        Raises:
            SpecificationError
                with error code :ref:`error-code-S101`. This is bubbled up by the `parse` method.
        """
        self.pattern = r"^(url|file|data): (.*)"
        self.fm = FileManager()
        self.hash_method = self.fm.hash_data
        self.extract: Dict[str, Callable[[str], str]] = {
            "file": self.fm.read,
            "url": self.fm.download,
            "data": lambda x: x,
        }
        res = self.check_path(file_path)
        file_contents = self.extract[res["method"]](res["path"])
        self.digest = self.hash_method(str(file_contents))
        self.contents = self.parse(file_contents)

    @typechecked
    def check_path(self, file_path: str) -> Dict[str, str]:
        """Check if the given path is adhearing to the spec.

        If it is complying with the specification then returns a dict
        with the `method` and the `path` which can be used to access
        the file.

        Args:
            file_path: The file path according to the spec

        Returns:
            Dict with `method` and `path`

        Raises:
            SpecificationError
                with code :ref:`error-code-S101`
        """
        try:
            result = re.match(self.pattern, file_path)
            assert result is not None
            return {"method": result.group(1), "path": result.group(2)}
        except AssertionError:
            raise e.SpecificationError(
                error=file_path,
                error_code="S101",
                message="The file_path you gave didn't start with a method.",
            )

    @classmethod
    def parse(cls, file_contents: str, file_format: str = "toml") -> Dict[Any, Any]:
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