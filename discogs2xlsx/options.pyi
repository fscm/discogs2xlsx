import argparse
from . import __project__, __version__
from . import DEFAULT_FILE_COLLECTION, DEFAULT_FILE_WANTLIST
from typing import Any, Optional

ArgumentParser = argparse.ArgumentParser
MutuallyExclusiveGroup: argparse._MutuallyExclusiveGroup
Namespace = argparse.Namespace


class _WantlistAction(argparse.Action):
    def __call__(
        self,
        parser: ArgumentParser,
        amespace: Namespace,
        values: list[str],
        option_string: Optional[str] = ...) -> None: ...


class Options:
    def __init__(self) -> None: ...
    def __setattr__(self, name: Any, value: Any) -> None: ...
    @property
    def all(self) -> dict[str, Any]: ...
