"""Folder module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller_core import base_module as bm


@dataclass
class FolderModule(bm.BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    requires: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    init: Optional[List[bm.ModuleInstallInstruction]] = None
    create: bool = True
    config: Optional[List[bm.ModuleInstallInstruction]] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
    rollback: bool = True

    def install(self):
        pass

    def uninstall(self):
        pass
