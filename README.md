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

## Pipenv

You will need `pipenv` installed in your machine. Pipenv is used to manage Python virtualenv and manage the application dependencies.

[Pipenv Github repository](https://github.com/pypa/pipenv)

Installing using

```sh
brew install pipenv
```

More instructions on their Github repository.

# Develop

Before you git push a new module make sure unit tests are also included. Test are to be written using `pytest`.

For more information look into [Test Driven Development](https://www.freecodecamp.org/news/test-driven-development-what-it-is-and-what-it-is-not-41fa6bca02a2/).

## For developers install normal and dev dependencies

```sh
pipenv install --dev
```

## Use pipenv shell

```sh
pipenv shell
```

## Run

To run the app

`cd` to the project root where `app.py` file is present, then run this on the terminal

```sh
flask run
```

## Install normal dependencies

```sh
pipenv install numpy
```

## Install dev dependencies

```sh
pipenv install pytest --dev
```

# Testing and code coverage

## Testing

Pop into pipenv shell and run:

```sh
coverage run
```

## Coverage report

Generate HTML based code coverage report:

```sh
coverage html
```

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

    | Option                | Value                               |
    | --------------------- | ----------------------------------- |
    | gitlab-ci coordinator | <https://gitlab.com>                |
    | gitlab-ci description | Enter some description              |
    | gitlab-ci tags        | Enter some tags                     |
    | Executer              | `docker`                            |
    | default docker image  | Enter the name of some docker image |

## Running the tests

```
gitlab-runner exec docker test
```

# Facing any problems

## Issue with installing pipenv packages

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

For more information Read the docs.

# Changelog

## Usage

```sh
git-chglog -o CHANGELOG.md
```

## More information

For more information Read the docs.

# Full Documentation

Read the docs.
