Usage
=====

Basic
-----

.. code:: bash

   dev install

Specify platform
----------------

.. code:: bash

   dev install --platform macos  # dev install -p macos

Specify both platform and desired preset
----------------------------------------

.. code:: bash

   dev install --platform macos --preset doom

Prerequisites
=============

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

Use poetry shell
----------------

.. code:: bash

   poetry shell

Install normal dependencies
---------------------------

.. code:: bash

   poetry add numpy

Install dev dependencies
------------------------

.. code:: bash

   poetry add -D pytest

Testing and code coverage
=========================

Testing
-------

Install `tox <https://tox.readthedocs.io/en/latest/index.html>`__ on
your machine globally or in a separate venv, then run:

.. code:: bash

   tox

Coverage report
---------------

Coverage report is automatically generated for the master branch by
`coveralls.io <https://coveralls.io/gitlab/justinekizhak/devinstaller>`__

Testing using Gitlab runner locally
===================================

.. _prerequisites-1:

Prerequisites
-------------

Docker
~~~~~~

You need docker installed, because we will be using the ``docker``
executor for the gitlab-runner.

Install ``gitlab-runner`` locally
---------------------------------

MacOS
~~~~~

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
-----------------

::

   gitlab-runner exec docker test

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

This project uses the `Conventional git commit
specs <https://www.conventionalcommits.org/en/v1.0.0/>`__.

More information
----------------

`Read the docs <https://devinstaller.readthedocs.io/en/latest/>`__

Changelog
=========

Changelog is generated using ``git-chglog``. See
`git-chglog <https://github.com/git-chglog/git-chglog>`__.

.. _usage-1:

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
