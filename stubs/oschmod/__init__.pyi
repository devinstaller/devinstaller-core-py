from typing import Any, Optional

IS_WINDOWS: Any
HAS_PYWIN32: bool
HAS_PWD: bool
W_FLDIR: Any
W_FADFL: Any
W_FADSD: Any
W_FRDEA: Any
W_FWREA: Any
W_FTRAV: Any
W_FDLCH: Any
W_FRDAT: Any
W_FWRAT: Any
W_DELET: Any
W_RDCON: Any
W_WRDAC: Any
W_WROWN: Any
W_SYNCH: Any
W_FGNEX: Any
W_FGNRD: Any
W_FGNWR: Any
W_GENAL: Any
W_GENEX: Any
W_GENWR: Any
W_GENRD: Any
W_DIRRD: Any
W_DIRWR: Any
W_DIREX: Any
W_FILRD = W_FGNRD
W_FILWR: Any
W_FILEX = W_FGNEX
WIN_RWX_PERMS: Any
WIN_FILE_PERMISSIONS: Any
WIN_DIR_PERMISSIONS: Any
WIN_DIR_INHERIT_PERMISSIONS: Any
WIN_ACE_TYPES: Any
WIN_INHERITANCE_TYPES: Any
SECURITY_NT_AUTHORITY: Any
FILE: int
DIRECTORY: int
OBJECT_TYPES: Any
OWNER: int
GROUP: int
OTHER: int
OWNER_TYPES: Any
READ: int
WRITE: int
EXECUTE: int
OPER_TYPES: Any
STAT_MODES: Any
STAT_KEYS: Any

def get_mode(path: Any): ...
def set_mode(path: Any, mode: Any): ...
def set_mode_recursive(path: Any, mode: Any, dir_mode: Optional[Any] = ...): ...
def get_effective_mode(current_mode: Any, symbolic: Any): ...
def get_object_type(path: Any): ...
def get_owner(path: Any): ...
def get_group(path: Any): ...
def win_get_owner_sid(path: Any): ...
def win_get_group_sid(path: Any): ...
def win_get_other_sid(): ...
def convert_win_to_stat(win_perm: Any, user_type: Any, object_type: Any): ...
def convert_stat_to_win(mode: Any, user_type: Any, object_type: Any): ...
def win_get_user_type(sid: Any, sids: Any): ...
def win_get_object_sids(path: Any): ...
def win_get_permissions(path: Any): ...
def win_set_permissions(path: Any, mode: Any) -> None: ...
def print_win_inheritance(flags: Any) -> None: ...
def print_mode_permissions(mode: Any) -> None: ...
def print_win_ace_type(ace_type: Any) -> None: ...
def print_win_permissions(win_perm: Any, flags: Any, object_type: Any) -> None: ...
def print_obj_info(path: Any) -> None: ...
def perm_test(mode: Any = ...) -> None: ...
