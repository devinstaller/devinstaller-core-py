[![img](https://img.shields.io/badge/Made_in-Doom_Emacs-blue?style=for-the-badge)](https://github.com/hlissner/doom-emacs)
[![img](https://img.shields.io/badge/follow_me-@alka1e-E4405F?style=for-the-badge&logo=instagram&labelColor=8f3c4c&logoColor=white)](https://www.instagram.com/alka1e)
[![img](https://img.shields.io/badge/follow_me-@alka1e-1DA1F2?style=for-the-badge&logo=twitter&labelColor=27597a&logoColor=white)](https://twitter.com/alka1e)

# Devinstaller

[![img](https://img.shields.io/badge/work_in-progress-eb3434?style=for-the-badge&labelColor=7d1616)]()
[![img](https://img.shields.io/badge/license-mit-blueviolet?style=for-the-badge)]()
[![Documentation Status](https://readthedocs.org/projects/devinstaller/badge/?version=latest&style=for-the-badge)](https://devinstaller.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gl/devinstaller/devinstaller/branch/master/graph/badge.svg)](https://codecov.io/gl/devinstaller/devinstaller)
[![pipeline](https://gitlab.com/justinekizhak/devinstaller/badges/master/pipeline.svg)](https://gitlab.com/devinstaller/devinstaller/-/commits/master)

## Table of Contents

[[_TOC_]]

# What is Devinstaller?

Devinstaller started its life as a dotfile manager but now its has developed into a unique tool to handle developer environments and their tools.

Unlike other tools which are static config files and they are interpreted and executed by some other application, Devinstaller lets you handle the interpretation and its execution.

# Features

- Native support for both Shell and Python commands
- Native support for other program language can be easily done by creating plugins
- Default config format is `toml` but `yaml` and `json` are also supported.
- Full control over the spec can be handed over
- Supports Importing other specifications

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

# Full Documentation

Main page: [Read the docs](https://devinstaller.readthedocs.io/en/latest/)

| Topic              | Documentation link                                                  |
| ------------------ | ------------------------------------------------------------------- |
| The Design process | <https://devinstaller.readthedocs.io/en/latest/design_process.html> |
| Terminology        | TODO                                                                |
| Specification      | <https://devinstaller.readthedocs.io/en/latest/specification.html>  |
| Rules              | TODO                                                                |
| CLI Commands       | TODO                                                                |
| Module guide       | TODO                                                                |
| Custom Interface   | TODO                                                                |
| Library guide      | TODO                                                                |
| API                | <https://devinstaller.readthedocs.io/en/latest/api.html>            |
| Contributing       | <https://devinstaller.readthedocs.io/en/latest/contributing.html>   |

_Remaining docs are WIP_

# License

Licensed under the terms of [MIT License](LICENSE.md)

---

[![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/approved-by-george-costanza.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/certified-snoop-lion.svg)](https://forthebadge.com)
