# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 19:06:45 IST
# Last-Updated: Fri  5 Jun 2020 18:42:45 IST
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

"""Houses all the custom exceptions in the app"""


class ParseError(ValueError):
    """Exception when a statement in the yaml field inside the devfile
    is not valid"""
    def __init__(self, statement, rule, message=""):
        self.statement = statement
        self.rule = rule
        super(ParseError, self).__init__(message)

    def __str__(self):
        return "Error parsing `{statement}`. Look into: {rule}".format(
            statement=self.statement, rule=self.rule
        )


class SchemaComplianceError(Exception):
    """Exception when a yaml field in the devfile is not valid"""
    def __init__(self, errors, message=""):
        self.errors = errors
        super(SchemaComplianceError, self).__init__(message)

    def __str__(self):
        return "{errors}".format(errors=self.errors)


class RuleViolation(Exception):
    """Exception when a runtime rule is violated"""
    def __init__(self, rule_code, rule_statement, message=""):
        self.rule_code = rule_code
        self.rule_statement = rule_statement
        super(RuleViolation, self).__init__(message)

    def __str__(self):
        return "I found a violation of rule {code}. The rule says: {statement}".format(
            code=self.rule_code, statement=self.rule_statement
        )