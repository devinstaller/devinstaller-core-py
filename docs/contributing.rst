============
Contributing
============

:Author: Justine Kizhakkinedath

Prerequisites
=============

These are requirements you need to install globally beforehand.

Python 3.8
----------

The project uses a lot of features on in the 3.8 version so you need
this. You can install this in any way you want, as long as ``poetry``
can reach it.

Poetry
------

You will need ``poetry`` installed in your machine. Poetry helps you
declare, manage and install dependencies of Python projects, ensuring
you have the right stack everywhere.

`Poetry Github repository <https://github.com/python-poetry/poetry>`__

Installing using

.. code:: bash

   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

More instructions on their Github repository.

Tox
---

You can run unit test and coverage report without tox, but tox makes it
easier. The CI/CD uses the tox setup so you can run the tests in the
same way the CI/CD will be running.

Develop
=======

Before you git push a new module make sure unit tests are also included.
Test are to be written using ``pytest``.

For more information look into `Test Driven
Development <https://www.freecodecamp.org/news/test-driven-development-what-it-is-and-what-it-is-not-41fa6bca02a2/>`__.

For developers install normal and dev dependencies
--------------------------------------------------

.. code:: bash

   poetry install

Install dev dependencies
------------------------

.. code:: bash

   poetry add -D pytest

Install normal dependencies
---------------------------

.. code:: bash

   poetry add numpy

Use poetry shell
----------------

.. code:: bash

   poetry shell

Testing
=======

Install `tox <https://tox.readthedocs.io/en/latest/index.html>`__ on
your machine globally or in a separate venv, then run:

.. code:: bash

   tox

Testing using Gitlab runner locally
-----------------------------------

Gitlab runner requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Docker You need docker installed, because we will be using the
   ``docker`` executor for the gitlab-runner.

Install ``gitlab-runner`` locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. MacOS

   #. Install using brew

      ::

         brew install gitlab-runner

   #. Register it with gitlab

      ::

         gitlab-runner register

   #. Options

      ========================= ===================================
      Option                    Value
      ========================= ===================================
      ``gitlab-ci coordinator`` https://gitlab.com
      ``gitlab-ci description`` Enter some description
      ``gitlab-ci tags``        Enter some tags
      ``Executer``              ``docker``
      ``default docker image``  Enter the name of some docker image
      ========================= ===================================

Running the tests
~~~~~~~~~~~~~~~~~

::

   gitlab-runner exec docker test

Coverage report
===============

Coverage report is automatically generated for the master branch by
`coveralls.io <https://coveralls.io/gitlab/justinekizhak/devinstaller>`__

Facing any problems
===================

Issue with installing poetry packages
-------------------------------------

Try setting LANG variable for the shell, if its not set.

Copy paste this line into your ``~/.bash_profile`` or ``~/.zshrc``.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   export $LANG = en_US.UTF-8

After this you might need to reopen the terminal.

Reinstall Python using brew
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default python installation from Xcode is not built using SSL
support. So you may have problem installing packages.

Reinstall python using this command on the terminal:

.. code:: bash

   brew reinstall python

Git
===

This project uses the `DEP 2
specification <https://gitlab.com/devinstaller/deps/-/tree/master/dep-0002>`__
for commit message format.

Changelog
=========

Changelog is generated using ``git-chglog``. See
`git-chglog <https://github.com/git-chglog/git-chglog>`__.

Usage
-----

.. code:: bash

   git-chglog -o CHANGELOG.md

Versioning
==========

This project uses `Semver versioning <https://semver.org/>`__.

Version management is done using ``poetry``.

Commands
--------

For more command check `poetry
versioning <https://python-poetry.org/docs/cli/#version>`__.

To bump up major version
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   poetry version major

To bump up minor version
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   poetry version minor

To bump up patch version
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   poetry version patch

Type checking
=============

You can type check this project. Type hints are provided.

To check you need ``tox``. You can install ``tox`` globally or in a
virtualenv.

.. code:: bash

   tox -e type

Stub generation
---------------

Type checking for external packages need stubs.

To generate stub pop into poetry shell and run:

.. code:: bash

   stubgen -p PACKAGE_NAME -o stubs

About the dependency files
==========================

There are 2 files used to store the dependency.

For developing the application
------------------------------

Both the dev and non dev dependencies are stored in the
``pyproject.toml``.

For building the docs
---------------------

Dependencies required for ReadTheDocs are in ``docs/reqirements.txt``.

There are 2 types of dependencies in the ``requirements.txt`` file

#. Sphinx dependencies These are required for building the docs
#. Dependencies for documentation linking These are required so that the
   Devinstaller docs can use the docs of the library it is using.

To get this list, run in the shell:

.. code:: bash

   poetry export -f requirements.txt --without-hashes
