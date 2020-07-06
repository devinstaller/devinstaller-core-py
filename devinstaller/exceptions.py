# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 19:06:45 IST
# Last-Updated: Mon  6 Jul 2020 19:38:44 IST
#
# exceptions.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: All the exceptions
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

"""Houses all the custom exceptions in the app
"""

rules = {
    100: (
        "You didn't provide the name of the current platform and I couldn't "
        "figure it out either."
    ),
    101: (
        "You didn't provide the name of the preset you want to install and I "
        "didn't found the name of the default preset in the spec."
    ),
    102: (
        "The name of the preset you gave through the cli didn't match with "
        "any preset in the spec file."
    ),
    103: (
        "The name of the default preset present in the spec didn't match "
        "with any preset in the file."
    ),
    104: ("There is an module record missing in a `required` list of another module."),
}


class ParseError(ValueError):
    """Exception when a statement in the yaml field inside the devfile
    is not valid
    """

    def __init__(self, error_statement: str, rule_code: int, message: str = "") -> None:
        self.error_statement = error_statement
        self.rule_code = rule_code
        self.message = message

    def __str__(self):
        return (
            f"{ self.message }Error parsing `{ self.error_statement }`. Look into: { self.rule_code }"
            f"Rule { self.rule_code }: {rules[self.rule_code]}"
        )


class SchemaComplianceError(ValueError):
    """Exception when a yaml field in the devfile is not valid
    """

    def __init__(self, errors: str, message: str = "") -> None:
        self.errors = errors
        self.message = message

    def __str__(self):
        return f"{ self.message }\n{ self.errors }"


class RuleViolationError(ValueError):
    """Exception when a runtime rule is violated
    """

    def __init__(self, rule_code: int, message: str = "") -> None:
        self.rule_code = rule_code
        self.message = message

    def __str__(self):
        return (
            f"{ self.message }\nI found a violation of rule { self.rule_code }."
            f"Rule { self.rule_code }: {rules[self.rule_code]}"
        )
