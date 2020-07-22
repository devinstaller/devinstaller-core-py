from typing import List

import questionary
from typeguard import typechecked


@typechecked
def ask_user_confirmation(title: str) -> bool:
    """Wrapper function around `questionary.confirm`

    Asks user for yes or no response.

    Args:
        title: The title you want to show to the user

    Returns:
        yes or no in boolean
    """
    return questionary.confirm(title).ask()


@typechecked
def ask_user_to_select(title: str, choices: List[str]) -> str:
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
def ask_user_for_multi_select(title: str, choices: List[str]) -> List[str]:
    """Wrapper function around `questionary.checkbox`

    Ask user to select all that which is applicable

    Args:
        title: The title for the choices
        choices: The statement for each choice

    Returns:
        The list of statements which have been selected by the user
    """
    return questionary.checkbox(title, choices).ask()
