"""Folder module
"""
import grp
import os
import pwd
import sys
from typing import List, Optional

import oschmod
from pydantic import validator
from pydantic.dataclasses import dataclass

from devinstaller_core import exception as e
from devinstaller_core import module_base as mb
from devinstaller_core import utilities as u

ui = u.UserInteraction()


@dataclass
class ModuleFolder(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    requires: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    inits: Optional[List[mb.ModuleInstallInstruction]] = None
    create: bool = True
    configs: Optional[List[mb.ModuleInstallInstruction]] = None
    owner: Optional[str] = None
    group: Optional[str] = None
    folder_path: Optional[str] = None
    permission: Optional[str] = None
    rollback: bool = True

    @validator("inits", "configs")
    @classmethod
    def replace_var_in_install_inst(
        cls, install_inst: Optional[List[mb.ModuleInstallInstruction]], values
    ) -> Optional[List[mb.ModuleInstallInstruction]]:
        """The validator method which will replace all the variables in the
        `install_inst` with the `constants`
        """
        constants = values["constants"]
        if install_inst is None:
            return None
        for i in install_inst:
            i.cmd = i.cmd.format(**constants)
        return install_inst

    def install(self):
        def core():
            """Core logic for creating folder
            """
            raw_path = self.folder_path if self.folder_path else self.name
            path = u.resolve_path(raw_path)
            os.makedirs(path)
            if self.owner and self.group:
                uid = pwd.getpwnam(self.owner).pw_uid
                gid = grp.getgrnam(self.group).gr_gid
                os.chown(path, uid, gid)
            if self.permission:
                oschmod.set_mode(path, self.permission)

        ui.print(f"Installing module: {self.display}...")
        # installation_steps = create_instruction_list(self.install_inst)
        try:
            self.execute_instructions(self.inits)
            core()
            self.execute_instructions(self.configs)
        except e.ModuleRollbackFailed:
            ui.print(
                f"Rollback instructions for {self.display} failed. Quitting program."
            )
            sys.exit(1)

    def uninstall(self):
        """Method to rollback if the installation failed and this module is now
        an orphan module.
        """
        if self.rollback:
            raw_path = self.folder_path if self.folder_path else self.name
            path = u.resolve_path(raw_path)
            os.removedirs(path)
