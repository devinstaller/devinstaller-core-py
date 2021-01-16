from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from pydantic import BaseModel, validator
from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller_core import command as c
from devinstaller_core import exception as e
from devinstaller_core import messages as m
from devinstaller_core import settings as s
from devinstaller_core import utilities as u

ui = u.UserInteraction()
session = c.SessionSpec()


@dataclass
class ModuleInstallInstruction:
    """The class used to convert `init`, `command` and `config` into objects"""

    cmd: str
    rollback: Optional[str] = None


@dataclass
class ModuleBase(ABC):
    """The class which will be used by all the modules"""

    # pylint: disable=too-many-instance-attributes
    name: str
    alias: Optional[str] = None
    display: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    constants: Optional[Dict[str, str]] = None

    @validator("alias", pre=True, check_fields=False)
    @classmethod
    def alias_validator(cls, alias: Optional[str], values) -> str:
        """Set the alias if it is not provided."""
        if alias is None:
            return values["name"]
        return alias

    @validator("display", pre=True, check_fields=False)
    @classmethod
    def display_validator(cls, display: Optional[str], values) -> str:
        """Set the display if it is not provided."""
        if display is None:
            return values["name"]
        return display

    @validator("constants", pre=True, check_fields=False)
    @classmethod
    def convert_constant(
        cls, constants: Optional[List[Dict[str, str]]]
    ) -> Dict[str, str]:
        """Convert incomming dict into dict which can be used for
        constants replacing.
        """
        data: Dict[str, str] = {}
        if constants is None:
            return {}
        for i in constants:
            data[i["key"]] = i["value"]
        return data

    def __str__(self) -> str:
        if self.description is None:
            return f"{self.display}"
        return f"{self.display} - {self.description}"

    @abstractmethod
    def install(self) -> None:
        """Abstract install function for each module to be immplemented"""
        pass

    @abstractmethod
    def uninstall(self) -> None:
        """Abstract uninstall function for each module to be immplemented"""
        pass

    @typechecked
    def execute_instructions(
        self, instructions: Optional[List[ModuleInstallInstruction]]
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

        def core_logic(task=None):
            for index in range(len(instructions)):
                inst = instructions[index]
                try:
                    session.run(inst.cmd)
                    if task is not None:
                        self.progress.update(task, advance=1)
                except e.CommandFailed:
                    rollback_list = instructions[:index]
                    rollback_list.reverse()
                    if task is not None:
                        self.progress.remove_task(task)
                    self.rollback_instructions(instructions, rollback_list)
                    raise e.ModuleInstallationFailed(error=inst.cmd, error_code="D103")

        if instructions == [] or instructions is None:
            return None
        self.progress = ui.track(transient=True)
        show_message = s.settings.DDOT_VERBOSE
        if show_message:
            core_logic()
            return
        with self.progress:
            task = self.progress.add_task("Running...", total=len(instructions))
            core_logic(task)

    @typechecked
    def rollback_instructions(
        self,
        instructions: List[ModuleInstallInstruction],
        rollback_instructions: List[ModuleInstallInstruction],
    ) -> None:
        """Rollback the installation of a module

        Args:
            List of install instructions

        Raises:
            ModuleRollbackFailed
                if the rollback instructions fails
        """
        show_message = s.settings.DDOT_VERBOSE
        ui.print(
            "\n"
            + m.error_message(
                f"There was some error in installing module: [red]{self.name}[/red],\n"
                "because of that I am rolling back all the changes so far."
            )
            + "\n"
        )
        show_message = s.settings.DDOT_VERBOSE
        if not show_message:
            task = self.progress.add_task("Rolling back...", total=len(instructions))
            self.progress.update(task, advance=len(rollback_instructions))
        for inst in rollback_instructions:
            if inst.rollback is not None:
                try:
                    ui.print(
                        m.warning_message(
                            f"Rolling back `{inst.cmd}` using `{inst.rollback}`"
                        )
                    ) if show_message else None
                    session.run(inst.rollback)
                except e.CommandFailed:
                    raise e.ModuleRollbackFailed
            if not show_message:
                self.progress.update(task, advance=-1)
