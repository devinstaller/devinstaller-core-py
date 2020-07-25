from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller.models.base_module import BaseModule, ModuleInstallInstruction


@dataclass
class FolderModule(BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    requires: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    init: Optional[List[ModuleInstallInstruction]] = None
    create: bool = True
    config: Optional[List[ModuleInstallInstruction]] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
    rollback: bool = True
