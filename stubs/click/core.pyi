from ._compat import PY2 as PY2, isidentifier as isidentifier, iteritems as iteritems, string_types as string_types
from .exceptions import Abort as Abort, BadParameter as BadParameter, ClickException as ClickException, Exit as Exit, MissingParameter as MissingParameter, UsageError as UsageError
from .formatting import HelpFormatter as HelpFormatter, join_options as join_options
from .globals import pop_context as pop_context, push_context as push_context
from .parser import OptionParser as OptionParser, split_opt as split_opt
from .termui import confirm as confirm, prompt as prompt, style as style
from .types import BOOL as BOOL, IntRange as IntRange, convert_type as convert_type
from .utils import PacifyFlushWrapper as PacifyFlushWrapper, echo as echo, get_os_args as get_os_args, make_default_short_help as make_default_short_help, make_str as make_str
from typing import Any, Optional

SUBCOMMAND_METAVAR: str
SUBCOMMANDS_METAVAR: str
DEPRECATED_HELP_NOTICE: str
DEPRECATED_INVOKE_NOTICE: str

def fast_exit(code: Any) -> None: ...
def batch(iterable: Any, batch_size: Any): ...
def invoke_param_callback(callback: Any, ctx: Any, param: Any, value: Any): ...
def augment_usage_errors(ctx: Any, param: Optional[Any] = ...) -> None: ...
def iter_params_for_processing(invocation_order: Any, declaration_order: Any): ...

class Context:
    parent: Any = ...
    command: Any = ...
    info_name: Any = ...
    params: Any = ...
    args: Any = ...
    protected_args: Any = ...
    obj: Any = ...
    default_map: Any = ...
    invoked_subcommand: Any = ...
    terminal_width: Any = ...
    max_content_width: Any = ...
    allow_extra_args: Any = ...
    allow_interspersed_args: Any = ...
    ignore_unknown_options: Any = ...
    help_option_names: Any = ...
    token_normalize_func: Any = ...
    resilient_parsing: Any = ...
    auto_envvar_prefix: Any = ...
    color: Any = ...
    show_default: Any = ...
    def __init__(self, command: Any, parent: Optional[Any] = ..., info_name: Optional[Any] = ..., obj: Optional[Any] = ..., auto_envvar_prefix: Optional[Any] = ..., default_map: Optional[Any] = ..., terminal_width: Optional[Any] = ..., max_content_width: Optional[Any] = ..., resilient_parsing: bool = ..., allow_extra_args: Optional[Any] = ..., allow_interspersed_args: Optional[Any] = ..., ignore_unknown_options: Optional[Any] = ..., help_option_names: Optional[Any] = ..., token_normalize_func: Optional[Any] = ..., color: Optional[Any] = ..., show_default: Optional[Any] = ...) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type: Any, exc_value: Any, tb: Any) -> None: ...
    def scope(self, cleanup: bool = ...) -> None: ...
    @property
    def meta(self): ...
    def make_formatter(self): ...
    def call_on_close(self, f: Any): ...
    def close(self) -> None: ...
    @property
    def command_path(self): ...
    def find_root(self): ...
    def find_object(self, object_type: Any): ...
    def ensure_object(self, object_type: Any): ...
    def lookup_default(self, name: Any): ...
    def fail(self, message: Any) -> None: ...
    def abort(self) -> None: ...
    def exit(self, code: int = ...) -> None: ...
    def get_usage(self): ...
    def get_help(self): ...
    def invoke(*args: Any, **kwargs: Any): ...
    def forward(*args: Any, **kwargs: Any): ...

class BaseCommand:
    allow_extra_args: bool = ...
    allow_interspersed_args: bool = ...
    ignore_unknown_options: bool = ...
    name: Any = ...
    context_settings: Any = ...
    def __init__(self, name: Any, context_settings: Optional[Any] = ...) -> None: ...
    def get_usage(self, ctx: Any) -> None: ...
    def get_help(self, ctx: Any) -> None: ...
    def make_context(self, info_name: Any, args: Any, parent: Optional[Any] = ..., **extra: Any): ...
    def parse_args(self, ctx: Any, args: Any) -> None: ...
    def invoke(self, ctx: Any) -> None: ...
    def main(self, args: Optional[Any] = ..., prog_name: Optional[Any] = ..., complete_var: Optional[Any] = ..., standalone_mode: bool = ..., **extra: Any): ...
    def __call__(self, *args: Any, **kwargs: Any): ...

class Command(BaseCommand):
    callback: Any = ...
    params: Any = ...
    help: Any = ...
    epilog: Any = ...
    options_metavar: Any = ...
    short_help: Any = ...
    add_help_option: Any = ...
    no_args_is_help: Any = ...
    hidden: Any = ...
    deprecated: Any = ...
    def __init__(self, name: Any, context_settings: Optional[Any] = ..., callback: Optional[Any] = ..., params: Optional[Any] = ..., help: Optional[Any] = ..., epilog: Optional[Any] = ..., short_help: Optional[Any] = ..., options_metavar: str = ..., add_help_option: bool = ..., no_args_is_help: bool = ..., hidden: bool = ..., deprecated: bool = ...) -> None: ...
    def get_usage(self, ctx: Any): ...
    def get_params(self, ctx: Any): ...
    def format_usage(self, ctx: Any, formatter: Any) -> None: ...
    def collect_usage_pieces(self, ctx: Any): ...
    def get_help_option_names(self, ctx: Any): ...
    def get_help_option(self, ctx: Any): ...
    def make_parser(self, ctx: Any): ...
    def get_help(self, ctx: Any): ...
    def get_short_help_str(self, limit: int = ...): ...
    def format_help(self, ctx: Any, formatter: Any) -> None: ...
    def format_help_text(self, ctx: Any, formatter: Any) -> None: ...
    def format_options(self, ctx: Any, formatter: Any) -> None: ...
    def format_epilog(self, ctx: Any, formatter: Any) -> None: ...
    def parse_args(self, ctx: Any, args: Any): ...
    def invoke(self, ctx: Any): ...

class MultiCommand(Command):
    allow_extra_args: bool = ...
    allow_interspersed_args: bool = ...
    no_args_is_help: Any = ...
    invoke_without_command: Any = ...
    subcommand_metavar: Any = ...
    chain: Any = ...
    result_callback: Any = ...
    def __init__(self, name: Optional[Any] = ..., invoke_without_command: bool = ..., no_args_is_help: Optional[Any] = ..., subcommand_metavar: Optional[Any] = ..., chain: bool = ..., result_callback: Optional[Any] = ..., **attrs: Any) -> None: ...
    def collect_usage_pieces(self, ctx: Any): ...
    def format_options(self, ctx: Any, formatter: Any) -> None: ...
    def resultcallback(self, replace: bool = ...): ...
    def format_commands(self, ctx: Any, formatter: Any) -> None: ...
    def parse_args(self, ctx: Any, args: Any): ...
    def invoke(self, ctx: Any): ...
    def resolve_command(self, ctx: Any, args: Any): ...
    def get_command(self, ctx: Any, cmd_name: Any) -> None: ...
    def list_commands(self, ctx: Any): ...

class Group(MultiCommand):
    commands: Any = ...
    def __init__(self, name: Optional[Any] = ..., commands: Optional[Any] = ..., **attrs: Any) -> None: ...
    def add_command(self, cmd: Any, name: Optional[Any] = ...) -> None: ...
    def command(self, *args: Any, **kwargs: Any): ...
    def group(self, *args: Any, **kwargs: Any): ...
    def get_command(self, ctx: Any, cmd_name: Any): ...
    def list_commands(self, ctx: Any): ...

class CommandCollection(MultiCommand):
    sources: Any = ...
    def __init__(self, name: Optional[Any] = ..., sources: Optional[Any] = ..., **attrs: Any) -> None: ...
    def add_source(self, multi_cmd: Any) -> None: ...
    def get_command(self, ctx: Any, cmd_name: Any): ...
    def list_commands(self, ctx: Any): ...

class Parameter:
    param_type_name: str = ...
    type: Any = ...
    required: Any = ...
    callback: Any = ...
    nargs: Any = ...
    multiple: bool = ...
    expose_value: Any = ...
    default: Any = ...
    is_eager: Any = ...
    metavar: Any = ...
    envvar: Any = ...
    autocompletion: Any = ...
    def __init__(self, param_decls: Optional[Any] = ..., type: Optional[Any] = ..., required: bool = ..., default: Optional[Any] = ..., callback: Optional[Any] = ..., nargs: Optional[Any] = ..., metavar: Optional[Any] = ..., expose_value: bool = ..., is_eager: bool = ..., envvar: Optional[Any] = ..., autocompletion: Optional[Any] = ...) -> None: ...
    @property
    def human_readable_name(self): ...
    def make_metavar(self): ...
    def get_default(self, ctx: Any): ...
    def add_to_parser(self, parser: Any, ctx: Any) -> None: ...
    def consume_value(self, ctx: Any, opts: Any): ...
    def type_cast_value(self, ctx: Any, value: Any): ...
    def process_value(self, ctx: Any, value: Any): ...
    def value_is_missing(self, value: Any): ...
    def full_process_value(self, ctx: Any, value: Any): ...
    def resolve_envvar_value(self, ctx: Any): ...
    def value_from_envvar(self, ctx: Any): ...
    def handle_parse_result(self, ctx: Any, opts: Any, args: Any): ...
    def get_help_record(self, ctx: Any) -> None: ...
    def get_usage_pieces(self, ctx: Any): ...
    def get_error_hint(self, ctx: Any): ...

class Option(Parameter):
    param_type_name: str = ...
    prompt: Any = ...
    confirmation_prompt: Any = ...
    hide_input: Any = ...
    hidden: Any = ...
    default: bool = ...
    is_flag: Any = ...
    flag_value: Any = ...
    type: Any = ...
    is_bool_flag: bool = ...
    count: Any = ...
    multiple: Any = ...
    allow_from_autoenv: Any = ...
    help: Any = ...
    show_default: Any = ...
    show_choices: Any = ...
    show_envvar: Any = ...
    def __init__(self, param_decls: Optional[Any] = ..., show_default: bool = ..., prompt: bool = ..., confirmation_prompt: bool = ..., hide_input: bool = ..., is_flag: Optional[Any] = ..., flag_value: Optional[Any] = ..., multiple: bool = ..., count: bool = ..., allow_from_autoenv: bool = ..., type: Optional[Any] = ..., help: Optional[Any] = ..., hidden: bool = ..., show_choices: bool = ..., show_envvar: bool = ..., **attrs: Any) -> None: ...
    def add_to_parser(self, parser: Any, ctx: Any) -> None: ...
    def get_help_record(self, ctx: Any): ...
    def get_default(self, ctx: Any): ...
    def prompt_for_value(self, ctx: Any): ...
    def resolve_envvar_value(self, ctx: Any): ...
    def value_from_envvar(self, ctx: Any): ...
    def full_process_value(self, ctx: Any, value: Any): ...

class Argument(Parameter):
    param_type_name: str = ...
    def __init__(self, param_decls: Any, required: Optional[Any] = ..., **attrs: Any) -> None: ...
    @property
    def human_readable_name(self): ...
    def make_metavar(self): ...
    def get_usage_pieces(self, ctx: Any): ...
    def get_error_hint(self, ctx: Any): ...
    def add_to_parser(self, parser: Any, ctx: Any) -> None: ...