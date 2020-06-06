# Devinstaller

[[_TOC_]]

# Usage

## Basic

```sh
dev install
```

## Specify platform

```sh
dev install --platform macos  # dev install -p macos
```

## Specify both platform and desired preset

```sh
dev install --platform macos --preset doom
```

# Prerequisites

## Poetry

You will need `poetry` installed in your machine. Poetry helps you declare, manage and install dependencies of Python projects, ensuring you have the right stack everywhere.

[Poetry Github repository](https://github.com/python-poetry/poetry)

Installing using

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

More instructions on their Github repository.

# Develop

Before you git push a new module make sure unit tests are also included. Test are to be written using `pytest`.

For more information look into [Test Driven Development](https://www.freecodecamp.org/news/test-driven-development-what-it-is-and-what-it-is-not-41fa6bca02a2/).

## For developers install normal and dev dependencies

```sh
poetry install
```

## Use poetry shell

```sh
poetry shell
```

## Install normal dependencies

```sh
poetry add numpy
```

## Install dev dependencies

```sh
poetry add -D pytest
```

# Testing and code coverage

## Testing

Install [tox](https://tox.readthedocs.io/en/latest/index.html) on your machine globally or in a separate venv, then run:

```sh
tox
```

## Coverage report

Coverage report is automatically generated for the master branch by [coveralls.io](https://coveralls.io/gitlab/justinekizhak/devinstaller)

# Testing using Gitlab runner locally

## Prerequisites

### Docker

You need docker installed, because we will be using the `docker` executor for the gitlab-runner.

## Install `gitlab-runner` locally

### MacOS

1.  Install using brew

    ```
    brew install gitlab-runner
    ```

2.  Register it with gitlab

    ```
    gitlab-runner register
    ```

3.  Options

    | Option                  | Value                               |
    | ----------------------- | ----------------------------------- |
    | `gitlab-ci coordinator` | <https://gitlab.com>                |
    | `gitlab-ci description` | Enter some description              |
    | `gitlab-ci tags`        | Enter some tags                     |
    | `Executer`              | `docker`                            |
    | `default docker image`  | Enter the name of some docker image |

## Running the tests

```
gitlab-runner exec docker test
```

# Facing any problems

## Issue with installing poetry packages

Try setting LANG variable for the shell, if its not set.

### Copy paste this line into your `~/.bash_profile` or `~/.zshrc`.

```sh
export $LANG = en_US.UTF-8
```

After this you might need to reopen the terminal.

### Reinstall Python using brew

The default python installation from Xcode is not built using SSL support. So you may have problem installing packages.

Reinstall python using this command on the terminal:

```sh
brew reinstall python
```

# Git

This project uses the [Conventional git commit specs](https://www.conventionalcommits.org/en/v1.0.0/).

## More information

[Read the docs](https://devinstaller.readthedocs.io/en/latest/)

# Versioning

This project uses [Semver versioning](https://semver.org/).

Version management is done using `poetry`.

## Commands

For more command check [poetry versioning](https://python-poetry.org/docs/cli/#version).

### To bump up major version

```sh
poetry version major
```

# Changelog

Changelog is generated using `git-chglog`. See [git-chglog](https://github.com/git-chglog/git-chglog).

## Usage

```sh
git-chglog -o CHANGELOG.md
```

## More information

[Read the docs](https://devinstaller.readthedocs.io/en/latest/)

# Full Documentation

[Read the docs](https://devinstaller.readthedocs.io/en/latest/)

Docs are auto generated on new commits on the master branch
