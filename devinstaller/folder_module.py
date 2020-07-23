from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller import base_module as b


@dataclass
class FolderModule(b.BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    requires: Optional[List[str]] = None
    optionals: Optional[List[str]] = None
    init: Optional[List[b.ModuleInstallInstruction]] = None
    create: bool = True
    config: Optional[List[b.ModuleInstallInstruction]] = None
    owner: Optional[str] = None
    parent_dir: Optional[str] = None
    permission: Optional[str] = None
    rollback: bool = True
