from .exceptions import BadArgumentUsage as BadArgumentUsage, BadOptionUsage as BadOptionUsage, NoSuchOption as NoSuchOption, UsageError as UsageError
from typing import Any, Optional

def split_opt(opt: Any): ...
def normalize_opt(opt: Any, ctx: Any): ...
def split_arg_string(string: Any): ...

class Option:
    prefixes: Any = ...
    dest: Any = ...
    action: Any = ...
    nargs: Any = ...
    const: Any = ...
    obj: Any = ...
    def __init__(self, opts: Any, dest: Any, action: Optional[Any] = ..., nargs: int = ..., const: Optional[Any] = ..., obj: Optional[Any] = ...) -> None: ...
    @property
    def takes_value(self): ...
    def process(self, value: Any, state: Any) -> None: ...

class Argument:
    dest: Any = ...
    nargs: Any = ...
    obj: Any = ...
    def __init__(self, dest: Any, nargs: int = ..., obj: Optional[Any] = ...) -> None: ...
    def process(self, value: Any, state: Any) -> None: ...

class ParsingState:
    opts: Any = ...
    largs: Any = ...
    rargs: Any = ...
    order: Any = ...
    def __init__(self, rargs: Any) -> None: ...

class OptionParser:
    ctx: Any = ...
    allow_interspersed_args: bool = ...
    ignore_unknown_options: bool = ...
    def __init__(self, ctx: Optional[Any] = ...) -> None: ...
    def add_option(self, opts: Any, dest: Any, action: Optional[Any] = ..., nargs: int = ..., const: Optional[Any] = ..., obj: Optional[Any] = ...) -> None: ...
    def add_argument(self, dest: Any, nargs: int = ..., obj: Optional[Any] = ...) -> None: ...
    def parse_args(self, args: Any): ...
