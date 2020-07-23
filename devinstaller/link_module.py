from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller import base_module as b


@dataclass
class LinkModule(b.BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    init: Optional[List[b.ModuleInstallInstruction]] = None
    config: Optional[List[b.ModuleInstallInstruction]] = None
    optionals: Optional[List[str]] = None
    owner: Optional[str] = None
    requires: Optional[List[str]] = None
    source: Optional[str] = None
    symbolic: Optional[bool] = None
    target: Optional[str] = None
    create: bool = True
    rollback: bool = True
