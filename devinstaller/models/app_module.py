"""App module
"""
import sys
from typing import List, Optional, Union

from pydantic import validator
from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller import commands as c
from devinstaller.exceptions import ModuleInstallationFailed, ModuleRollbackFailed
from devinstaller.models import base_module


@dataclass
class AppModule(base_module.BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    version: Optional[str] = None
    executable: Optional[str] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    install_inst: Optional[List[base_module.ModuleInstallInstruction]] = None
    uninstall_inst: Optional[List[str]] = None
    bind: Optional[List[str]] = None

    def __post_init_post_parse__(self):
        if self.install_inst is None:
            return None
        for i in self.install_inst:
            i.cmd = i.cmd.format(**self.constants)
            i.rollback = (
                i.rollback.format(**self.constants) if i.rollback is not None else None
            )
        if self.uninstall_inst is None:
            return None
        for i in self.uninstall_inst:
            i = i.format(**self.constants)

    def install(self) -> None:
        """The function which installs app modules

        Args:
            module: The app module

        Returns:
            The response object of the module
        """
        print(f"Installing module: {self.display}...")
        # installation_steps = create_instruction_list(self.install_inst)
        try:
            self.execute_instructions(self.install_inst)
        except ModuleRollbackFailed:
            print(f"Rollback instructions for {self.display} failed. Quitting program.")
            sys.exit(1)

    def uninstall(self) -> None:
        """Uninstall the module using its rollback instructions.

        Args:
            module: The module which you want to uninstall
        """
        print(f"Uninstalling module: {self.display}...")
        if self.uninstall_inst is None:
            print(f"No uninstallation instructions found for {self.display}.")
            return None
        try:
            for i in self.uninstall_inst:
                c.run(i)
        except ModuleInstallationFailed:
            print(f"Uninstallation of {self.display} failed. Quitting program.")
            sys.exit(1)
