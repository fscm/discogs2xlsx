from . import __project__ as __project__
from enum import IntEnum
from typing import Optional


class Logger:
    class Level(IntEnum):
        DEBUG: int = ...
        INFO: int = ...
        WARNING: int = ...
        ERROR: int = ...
        CRITICAL: int = ...
        NONE: int = ...

    def __init__(
        self,
        level: Level = ...,
        file: Optional[str] = ...) -> None: ...

    @property
    def file(self) -> str: ...
    @property
    def level(self) -> Level: ...
    def critical(self, msg: str) -> None: ...
    def debug(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...
    def info(self, msg: str) -> None: ...
    def warning(self, msg: str) -> None: ...
