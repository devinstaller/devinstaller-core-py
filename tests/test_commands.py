# -----------------------------------------------------------------------------
# Created: Wed  3 Jun 2020 03:00:14 IST
# Last-Updated: Wed 22 Jul 2020 18:08:17 IST
#
# test_commands.py is part of devinstaller
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
import shlex

import pytest

from devinstaller import commands as c
from devinstaller import exceptions as e


def test_command_run(fake_process):
    with pytest.raises(e.CommandFailed):
        command = "dev --version"
        mock_command = shlex.split(command)
        fake_process.register_subprocess(mock_command, returncode=1)
        c.run(command)
