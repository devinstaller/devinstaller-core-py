from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller.models.base_module import BaseModule


@dataclass
class GroupModule(BaseModule):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
