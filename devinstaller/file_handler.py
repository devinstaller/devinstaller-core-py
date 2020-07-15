# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:40:37 IST
# Last-Updated: Tue 14 Jul 2020 19:22:16 IST
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

import anymarkup


def read(file_path: str) -> dict:
    """Reads the file at the path and returns the data as dict object

    Args:
        file_path: The path to the file

    Returns:
        Python object

    Raises:
        ValueError: If the anymarkup syntax is invalid
    """
    with open(file_path, "r") as stream:
        try:
            return anymarkup.parse(stream)
        except Exception:
            raise ValueError(
                "Couln't load up your devfile. Somethings wrong with your anymarkup syntax"
            )


def parse_and_download(input_str: str):

    pass
