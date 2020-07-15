# Devinstaller

[![status alpha](https://img.shields.io/badge/status-ALPHA-critical?style=for-the-badge&labelColor=gray)](https://gitlab.com/justinekizhak/devinstaller)

---

[![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/approved-by-george-costanza.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/certified-snoop-lion.svg)](https://forthebadge.com)

[[_TOC_]]

# Table of Contents

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

| Topic            | Documentation link   |
| ---------------- | -------------------- |
| The Motivation   | Draft                |
| Terminology      | TODO                 |
| Specification    | Draft                |
| Rules            | TODO                 |
| Commands         | TODO                 |
| Module guide     | TODO                 |
| Custom Interface | TODO                 |
| Library guide    | TODO                 |
| API              | WIP (Auto generated) |
| Contributing     | Draft                |

# License

Licensed under the terms of [MIT License](LICENSE.md)
