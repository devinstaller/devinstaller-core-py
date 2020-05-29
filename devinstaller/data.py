# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Fri 29 May 2020 16:47:24 IST
#
# data.py is part of devinstaller
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
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "software"), to deal
#   in the software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the software, and to permit persons to whom the software is
#   furnished to do so, subject to the following conditions:
#
#   the above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the software.
#
#   the software is provided "as is", without warranty of any kind,
#   express or implied, including but not limited to the warranties of
#   merchantability, fitness for a particular purpose and noninfringement.
#   in no event shall the authors or copyright holders be liable for any claim,
#   damages or other liability, whether in an action of contract, tort or
#   otherwise, arising from, out of or in connection with the software or the use
#   or other dealings in the software.
# -----------------------------------------------------------------------------


rules = {
    "100": "Rule 100: You didn't provide the name of the current platform and I couldn't figure it out either.",
    "101": "Rule 101: You didn't provide the name of the preset you want to install and I didn't found the name of the default preset in the spec.",
    "102": "Rule 102: The name of the preset you gave through the cli didn't match with any preset in the spec file.",
    "103": "Rule 103: The name of the default preset present in the spec didn't match with any preset in the file.",
    "104": "Rule 104: There is an entry missing for a required module."
}

errors = {
    "500": "Something went terribly wrong."
}
