==================
The Implementation
==================

Introduction
============

The Devinstaller system consist of 3 parts:

The specification file
----------------------

It is refered as the ``spec`` file. Defaults to: ``devfile.toml``

The specification file is your static, declarative config file.

This is the meat of the system. When you run the command the runtime
starts looking for the spec file in you current directory.

First the runtime loads up the file and validates it. Once that's done
based on your commands it starts the execution cycle.

The execution cycle is where it gets interesting but we will talk that
later.

There are 2 ways to use other programming languages:

#. Native support
#. Handing over the execution cycle

The program file
----------------

It is refered as the ``prog`` file. Defaults to ``devfile.py``.

This forms the interface between the spec and the runtime.

The Devinstaller runtime
------------------------

It is refered as the ``runtime``.

The part which executes the instructions.

The runtime consist of 2 parts:

The runtime core
~~~~~~~~~~~~~~~~

It is refered as the ``core``.

The core contains only the logic required for the validation of the spec
and starting the execution cycle.

The execution handler
~~~~~~~~~~~~~~~~~~~~~

This is what most of the application code consists of.
