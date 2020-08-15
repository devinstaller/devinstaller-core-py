"""Link module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller_core import base_module as bm


@dataclass
class LinkModule(bm.BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    init: Optional[List[bm.ModuleInstallInstruction]] = None
    config: Optional[List[bm.ModuleInstallInstruction]] = None
    optionals: Optional[List[str]] = None
    owner: Optional[str] = None
    requires: Optional[List[str]] = None
    source: Optional[str] = None
    symbolic: Optional[bool] = None
    target: Optional[str] = None
    create: bool = True
    rollback: bool = True

    def install(self):
        pass

    def uninstall(self):
        pass
