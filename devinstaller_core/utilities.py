from typing import Any, Dict, List

import questionary
from typeguard import typechecked


class UserInteract:
    """All the methods you need for interacting with the users.

    You can do things like ask user for confirmation, single select
    or multiple select
    """

    @typechecked
    def confirm(self, title: str) -> bool:
        """Wrapper function around `questionary.confirm`

        Asks user for yes or no response.

        Args:
            title: The title you want to show to the user

        Returns:
            yes or no in boolean
        """
        return questionary.confirm(title).ask()

    @typechecked
    def select(self, title: str, choices: List[str]) -> str:
        """Wrapper function around `questionary.select`

        Asks user to select one of the choices.

        Args:
            title: The title for the choices
            choices: The statement for each choice

        Returns:
            The statement of the selected choice
        """
        return questionary.select(title, choices).ask()

    @typechecked
    def checkbox(self, title: str, choices: List[str]) -> List[str]:
        """Wrapper function around `questionary.checkbox`

        Ask user to select all that which is applicable

        Args:
            title: The title for the choices
            choices: The statement for each choice

        Returns:
            The list of statements which have been selected by the user
        """
        return questionary.checkbox(title, choices).ask()


class Dictionary:
    @classmethod
    @typechecked
    def remove_key(cls, input_dictionary: Dict[Any, Any], key: str) -> Dict[Any, Any]:
        """Remove the key and its value from the dictionary

        The original dictionary is not modified instead a copy is made
        and modified and that is returned.

        Args:
            input_dictionary: Any dictionary
            key: The key and its value you want to remove

        Returns:
            A new dictionary without the specified key
        """
        if key not in input_dictionary:
            return input_dictionary
        new_dictionary = input_dictionary.copy()
        new_dictionary.pop(key)
        return new_dictionary


class Compare:
    """All the methods you need to compare stuffs.
    """

    @typechecked
    def strings(self, *args: str) -> bool:
        """Compare all the strings with each other (case insensitive)

        Takes in any number of string arguments.
        At least one argument required else it will return False.
        If one argument then it will return True.

        Returns:
            True if all matches else False
        """
        if len({v.casefold() for v in args}) != 1:
            return False
        return True

    @typechecked
    def version(self, version: str, expected_version: str) -> bool:
        """Compares the version of the current platform and the version info in the spec file.

        TODO Works with both the platforms block and the modules block?
        TODO How to compare using the semver specification.
        TODO What about the modules which doesnt' use the semver spec?

        Uses the semver specification to compare.
        """
        if version == expected_version:
            return True
        return False
