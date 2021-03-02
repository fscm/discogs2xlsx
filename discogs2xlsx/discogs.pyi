from . import __project__ as __project__
from .logger import Logger as Logger
from requests import sessions
from typing import Any, Final, Optional

Session = sessions.Session


class Discogs:
    API_BASEURL: Final[str] = ...
    API_FORMAT: Final[str] = ...
    API_LIMIT: Final[int] = ...
    API_RATELIMIT_STATUS: Final[int] = ...
    API_RATELIMIT_TIME: Final[int] = ...

    def __init__(
        self,
        key: str,
        currency: Optional[str] = ...,
        logger: Optional[Logger] = ...) -> None: ...

    def get_collection(
        self,
        details: Optional[bool] = ...,
        prices: Optional[bool] = ...) -> dict[str, Any]: ...

    def get_wantlist(self, details: bool = ..., prices: bool = ...): ...
