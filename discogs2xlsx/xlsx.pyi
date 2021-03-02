from . import __project__ as __project__
from .logger import Logger as Logger
from typing import Any, Optional

Workbook = xlsxwriter.workbook.Workbook
Worksheet = xlsxwriter.worksheet.Worksheet


class Xlsx:
    def __init__(self, logger: Optional[Logger] = ...) -> None: ...

    def save_collection(
        self,
        collection: dict[str, Any],
        to_file: str) -> None: ...

    def save_wantlist(
        self,
        wantlist: dict[str, Any],
        to_file: str) -> None: ...
