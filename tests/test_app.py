# -----------------------------------------------------------------------------
# Created: Fri 29 May 2020 15:10:09 IST
# Last-Updated: Fri 29 May 2020 18:59:46 IST
#
# test_app.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Testing
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

from click.testing import CliRunner
from devinstaller.main import main


def test_install():
    runner = CliRunner()
    result = runner.invoke(main, ["install"])
    assert result.exit_code == 0


def test_list():
    runner = CliRunner()
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0


def test_run():
    runner = CliRunner()
    result = runner.invoke(main, ["run", "brew install emacs"])
    assert result.exit_code == 0
    assert result.output == "All good\n"
