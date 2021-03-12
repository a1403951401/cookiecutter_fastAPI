from typing import Any, overload, Dict


class BaseLogger:
    globals: Dict[str, Any]

    def __setitem__(self, key: str, value: Any) -> None: ...

    def __getitem__(self, key: str) -> Any: ...

    class bin:
        kwargs: Dict[str, Any]

        def __init__(self, **kwargs) -> None: ...

        def __enter__(self, **kwargs) -> logger: ...

        def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    @overload
    def trace(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def trace(self, __message: Any) -> None: ...

    @overload
    def debug(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def debug(self, __message: Any) -> None: ...

    @overload
    def info(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def info(self, __message: Any) -> None: ...

    @overload
    def success(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def success(self, __message: Any) -> None: ...

    @overload
    def warning(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def warning(self, __message: Any) -> None: ...

    @overload
    def error(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def error(self, __message: Any) -> None: ...

    @overload
    def critical(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def critical(self, __message: Any) -> None: ...

    @overload
    def exception(self, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def exception(self, __message: Any) -> None: ...

    @overload
    def log(self, __level: str, __message: str, *args: Any, **kwargs: Any) -> None: ...

    @overload
    def format_message(self, __message, *args, **kwargs) -> str: ...


logger: BaseLogger
