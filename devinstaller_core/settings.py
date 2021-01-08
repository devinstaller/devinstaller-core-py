from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    DDOT_VERBOSE = False


settings = Settings()


def get_env(key: str) -> str:
    """Get the environment value for a given key

    Args:
        key (str): The name of the environment variable

    Returns:
        str: Its value
    """
    return os.environ[key]


def set_env(key: str, value: str) -> None:
    """Set the value for the given key

    Args:
        key (str): The key of the environment variable
        value (str): The value for that variable
    """
    os.environ[key] = value
