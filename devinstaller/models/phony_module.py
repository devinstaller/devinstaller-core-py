"""Phony module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller.models.base_module import BaseModule, ModuleInstallInstruction


@dataclass
class PhonyModule(BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    config: Optional[List[ModuleInstallInstruction]] = None

    def install(self):
        pass

    def uninstall(self):
        pass
