from typing import Any, Final, Optional, TypeVar

Logger = TypeVar('Logger')

class DiscogsException(Exception): ...

class _DiscogsSession:
    API_BASEURL: Final[str]
    API_FORMAT: Final[str]
    API_LIMIT: Final[int]
    API_RATELIMIT: Final[int]
    API_RATELIMIT_STATUS: Final[int]
    API_RATELIMIT_TIME: Final[int]
    API_UNAUTHORIZED_STATUS: Final[int]
    def __init__(self, token: str, user_agent: Optional[str] = ...) -> None: ...
    def get(self, path: str, params: Optional[dict[str, Any]] = ...) -> dict[str, Any]: ...

class Discogs:
    def __init__(self, token: str, user_agent: Optional[str] = ..., currency: Optional[str] = ..., logger: Optional[Logger] = ...) -> None: ...
    def get_collection(self, details: Optional[bool] = ..., prices: Optional[bool] = ...) -> dict[str, Any]: ...
    def get_wantlist(self, details: Optional[bool] = ..., prices: Optional[bool] = ...) -> dict[str, Any]: ...
