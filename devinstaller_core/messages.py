WARNING_COLOR_HEX = "#FFA500"


def warning_message(message: str) -> str:
    return f"\n[{WARNING_COLOR_HEX}]WARNING[/{WARNING_COLOR_HEX}]: :disappointed_relieved: {message}"


def error_message(message: str) -> str:
    return f"\n[red]ERROR[/red]: :sob: {message}"

