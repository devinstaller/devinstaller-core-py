from typing import Any, List

import questionary
import rich
from typeguard import typechecked
from rich.progress import Progress

from devinstaller_core import extension as ex


console = rich.console.Console()


class ExtUserInteraction(ex.ExtUserInteraction):
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

    def print(self, *args, **kwargs) -> None:
        """Wrapper for printing rich text in the console

        Args:
            message: The object you want to display
        """
        console.print(*args, **kwargs)

    def status(self, *args, **kwargs):
        """Wrapper for `rich.status`.

        Show a spinner for tasks whose progress is difficult to calculate.
        """
        return console.status(*args, **kwargs)

    def track(self, *args, **kwargs):
        """Wrapper for `rich.track`.

        Track the progress for a list of tasks
        """
        return Progress(*args, **kwargs)
