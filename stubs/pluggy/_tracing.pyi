from typing import Any

class TagTracer:
    indent: int = ...
    def __init__(self) -> None: ...
    def get(self, name: Any): ...
    def setwriter(self, writer: Any) -> None: ...
    def setprocessor(self, tags: Any, processor: Any) -> None: ...

class TagTracerSub:
    root: Any = ...
    tags: Any = ...
    def __init__(self, root: Any, tags: Any) -> None: ...
    def __call__(self, *args: Any) -> None: ...
    def get(self, name: Any): ...
