"""Platform model
"""
import platform
from typing import List, Optional

from typeguard import typechecked

from devinstaller.exceptions import SpecificationError
from devinstaller.models.common_models import TypePlatform, TypePlatformInfo
from devinstaller.utilities import Compare, UserInteract


class Platform:
    """Class for creating the current platform object
    """

    @typechecked
    def __init__(
        self,
        platform_list: Optional[List[TypePlatform]] = None,
        platform_codename: Optional[str] = None,
    ) -> None:
        """Main function to get the platform object.

        Steps:
            1. If `platform_code_name` is provided then that is used to get the platform object
            2. If not present then current platform is checked against all the platforms defined

        Args:
            full_document: The full spec file
            platform_code_name: name of the platform

        Returns:
            The platform object
        """
        self.info: TypePlatformInfo = get_current_platform()
        self.codename: str = "MOCK"
        if not platform_codename:
            if platform_list is None:
                return None
            self.check_platform(platform_list)
            return None
        self.set_platform(platform_codename, platform_list=platform_list)
        return None

    @typechecked
    def set_platform(
        self, platform_codename: str, platform_list: List[TypePlatform]
    ) -> None:
        """Returns the platform object whose name matches the `platform_codename`.

        Args:
            full_document: The full spec file
            platform_codename: name of the platform

        Raises:
            SpecificationError
                with error code :ref:`error-code-S100`
        """
        for _plat in platform_list:
            if _plat["name"] == platform_codename:
                self.codename = platform_codename
                return None
        raise SpecificationError(
            platform_codename, "S100", "You are missing a platform"
        )

    @typechecked
    def check_platform(self, platform_list: List[TypePlatform]) -> None:
        """Gets the current platform code name

        Args:
            platform_list: List of all platforms declared in the spec
            current_platform: The current platform object

        Returns:
            The `code_name` of current platform
        """
        platforms_supported: List[TypePlatform] = []
        for _p in platform_list:
            _p_info: TypePlatformInfo = _p["platform_info"]
            if Compare.strings(_p_info["system"], self.info["system"]):
                if "version" not in _p_info:
                    platforms_supported.append(_p)
                elif Compare.version(_p_info["version"], self.info["version"]):
                    platforms_supported.append(_p)
        if len(platforms_supported) == 1:
            print(f"I see you are using {platforms_supported[0]['name']}")
            self.codename = platforms_supported[0]["name"]
            return None
        self.resolve(platforms_supported)
        return None

    @typechecked
    def resolve(self, platforms_supported: List[TypePlatform]) -> None:
        """Ask the user for which platform to be used.

        Sometimes it may happen that platform code name is not provided by the user so the
        system tries to figure which platform it is currently running.

        But it may happen that multiple platforms defined satisfy the conditions, in that case
        we will explicitly ask the user to select one of the platforms which are satisfied.

        Args:
            platforms_supported: List of platform objects which satisfies the condition

        Returns:
            The required platform object
        """
        print(
            'Hey.. your current platform supports multiple "platform" declared in the spec file'
        )
        title = "Do you mind narrowring it down to one for me?"
        choices = [p["name"] for p in platforms_supported]
        selection = UserInteract.select(title, choices)
        self.codename = selection


@typechecked
def get_current_platform() -> TypePlatformInfo:
    """Get the current platform object

    Returns:
        The current platform object
    """
    data: TypePlatformInfo = {
        "system": platform.system(),
        "version": platform.version(),
    }
    if data["system"] == "Darwin":
        data["version"] = platform.mac_ver()[0]
    return data
