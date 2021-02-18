from . import __project__ as __project__
from typing import Any, Optional
from .logger import Logger

class Xlsx:
    def __init__(self, logger: Optional[Logger] = ...) -> None: ...

    def save_collection(
        self, collection: dict[str, Any], to_file: str) -> None: ...

    def save_wantlist(
        self, wantlist: dict[str, Any], to_file: str) -> None: ...
