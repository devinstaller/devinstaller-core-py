import sys
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller.exceptions import ModuleRollbackFailed
from devinstaller.models.base_module import BaseModule, ModuleInstallInstruction
from devinstaller.utilities import create_instruction_list


@dataclass
class AppModule(BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    version: Optional[str] = None
    executable: Optional[str] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    init: Optional[List[ModuleInstallInstruction]] = None
    command: Optional[ModuleInstallInstruction] = None
    config: Optional[List[ModuleInstallInstruction]] = None

    def install(self) -> None:
        """The function which installs app modules

        Args:
            module: The app module

        Returns:
            The response object of the module
        """
        print(f"Installing module: {self.display}...")
        installation_steps = create_instruction_list(
            self.init, self.command, self.config
        )
        try:
            self.execute_instructions(installation_steps)
        except ModuleRollbackFailed:
            print(f"Rollback instructions for {self.display} failed. Crashing program.")
            sys.exit(1)
        return None

    def uninstall(self) -> None:
        """Uninstall the module using its rollback instructions.

        Args:
            module: The module which you want to uninstall
        """
        print(f"Uninstalling module: {self.display}...")
        uninstallation_steps = create_instruction_list(
            self.init, self.command, self.config
        ).reverse()
        try:
            self.rollback_instructions(uninstallation_steps)
        except ModuleRollbackFailed:
            print(f"Rollback instructions for {self.display} failed. Crashing program.")
            sys.exit(1)
        return None
