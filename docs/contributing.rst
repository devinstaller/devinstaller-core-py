============
Contributing
============

:Author: Justine Kizhakkinedath

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
