# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Wed 10 Jun 2020 21:53:26 IST
#
# models.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Contains all the app data
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

"""All the models including the schema as well as graph models"""

from typing import List, Optional
from devinstaller import exceptions as e
from pydantic.dataclasses import dataclass


@dataclass
class VersionBlock:
    """Class containing the info necessary to get the version info"""

    response: str
    command: str


@dataclass
class Module:
    """Common class for all modules"""

    name: str
    type: str
    installed: bool
    alias: Optional[str] = None
    display: Optional[str] = None
    command: Optional[str] = None
    config: Optional[List[str]] = None
    init: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    version: Optional[VersionBlock] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
