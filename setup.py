from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="devinstaller",
    version="0.1.0",
    author="Justine Kizhakkinedath",
    author_email="justine@kizhak.com",
    description="A Python package to setup your development environment \
    and manage all your dotfiles, software and packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/justinekizhak/devinstaller",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords="dotfile manager",
    entry_points={"console_scripts": ["dev=devinstaller.main:main"],},
    include_package_data=True,
    install_requires=[
        'cerberus',
        'pyyaml'
    ],
    project_urls={
        "Bug Reports": "https://gitlab.com/justinekizhak/devinstaller/issues",
        "Say Thanks!": "https://saythanks.io/to/justine%40kizhak.com",
        "Source": "https://gitlab.com/justinekizhak/devinstaller",
    },

)
