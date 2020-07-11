from devinstaller import file_handler as f
from devinstaller import schema as s


def install(file_name: str, platform: str, group: str) -> None:
    """Install the default preset and the modules which it requires.
    """
    file_path = file_name
    full_document = s.validate(f.read(file_path))
    s.extract(full_document, platform, group)


def show(file_name: str) -> None:
    """Show all the groups and modules available for your OS.
    """
    # TODO
    file_path = file_name
    full_document = s.validate(f.read(file_path))
    pass
