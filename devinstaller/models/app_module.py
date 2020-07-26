"""App module
"""
import sys
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller import commands as c
from devinstaller.exceptions import ModuleInstallationFailed, ModuleRollbackFailed
from devinstaller.models.base_module import BaseModule, ModuleInstallInstruction

# @typechecked
# def create_instruction_list(
#     *data: Union[ModuleInstallInstruction, List[ModuleInstallInstruction], None],
# ) -> List[ModuleInstallInstruction]:
#     """Returns a list with all the data combined.

#     This is used to combine the `init`, `command` and `config` instructions so
#     that they can be run in a single function.

#     Any number of arguments. The arguments are expected to be of either
#     ModuleInstallInstruction or list of ModuleInstallInstruction
#     """
#     temp_list = []
#     for i in data:
#         if i is not None:
#             if isinstance(i, list):
#                 temp_list += i
#             else:
#                 temp_list.append(i)
#     return temp_list


@dataclass
class AppModule(BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    version: Optional[str] = None
    executable: Optional[str] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    install_inst: Optional[List[ModuleInstallInstruction]] = None
    uninstall_inst: Optional[List[str]] = None

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
