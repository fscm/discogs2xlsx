from argparse import Action, ArgumentParser, Namespace
from typing import Any, Optional

class _EnvDefault(Action):
    def __init__(self, env_var: str, required: Optional[bool] = ..., default: Optional[Any] = ..., **kwargs) -> None: ...
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: list[str], option_string: Optional[str] = ...) -> None: ...

class _WantlistFile(Action):
    def __init__(self, target: str, **kwargs) -> None: ...
    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: list[str], option_string: Optional[str] = ...) -> None: ...

class Options:
    def __init__(self, name: str, version: str, parser: ArgumentParser = ...) -> None: ...
    @property
    def all(self) -> dict[str, Any]: ...
