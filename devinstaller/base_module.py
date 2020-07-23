from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller import commands as c
from devinstaller import exceptions as e


@dataclass
class ModuleInstallInstruction:
    """The class used to serialize`init`, `command` and `config` commands into objects
    """

    install: str
    rollback: Optional[str] = None


@dataclass
class BaseModule:
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    name: str
    alias: Optional[str] = None
    display: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None

    def __str__(self) -> str:
        if self.description is None:
            return f"{self.display}"
        return f"{self.display} - {self.description}"

    def install(self) -> None:
        raise NotImplementedError

    def uninstall(self) -> None:
        raise NotImplementedError

    def __post_init_post_parse__(self):
        if self.alias is None:
            self.alias = self.name
        if self.display is None:
            self.display = self.name

    @typechecked
    def execute_instructions(
        self, instructions: List[ModuleInstallInstruction]
    ) -> None:
        """The function which handles installing of multi step commands.

        Args:
            steps: The list of steps which needs to be executed

        Raises:
            ModuleInstallationFailed
                if the installation of the module fails
            ModuleRollbackFailed
                if the rollback command fails
        """
        if instructions == []:
            return None
        for index, inst in enumerate(instructions):
            try:
                c.run(inst.install)
            except e.CommandFailed:
                rollback_list = instructions[:index]
                rollback_list.reverse()
                try:
                    self.rollback_instructions(rollback_list)
                except e.ModuleRollbackFailed:
                    raise e.ModuleRollbackFailed
                raise e.ModuleInstallationFailed
        return None

    @typechecked
    def rollback_instructions(
        self, instructions: List[ModuleInstallInstruction]
    ) -> None:
        """Rollback the installation of a module

        Args:
            List of install instructions

        Raises:
            ModuleRollbackFailed
                if the rollback instructions fails
        """
        for inst in instructions:
            if inst.rollback is not None:
                try:
                    print(f"Rolling back `{inst.install}` using `{inst.rollback}`")
                    c.run(inst.rollback)
                except e.CommandFailed:
                    raise e.ModuleRollbackFailed
        return None
