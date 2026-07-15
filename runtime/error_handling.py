from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class RuntimeErrorType(Enum):

    UNKNOWN = "unknown"

    VALIDATION = "validation"

    PROVIDER = "provider"

    NETWORK = "network"

    TIMEOUT = "timeout"

    INTERNAL = "internal"


@dataclass(slots=True)
class RuntimeErrorInfo:
    """
    Normalized runtime error model.
    """

    error_type: RuntimeErrorType

    message: str

    exception_name: str

    recoverable: bool = False

    metadata: Dict[str, Any] = field(
        default_factory=dict,
    )


class RuntimeErrorHandler:
    """
    Runtime exception classifier.
    """

    def classify(
        self,
        exception: Exception,
    ) -> RuntimeErrorInfo:

        name = exception.__class__.__name__

        if isinstance(
            exception,
            TimeoutError,
        ):

            error_type = (
                RuntimeErrorType.TIMEOUT
            )

            recoverable = True

        elif isinstance(
            exception,
            ConnectionError,
        ):

            error_type = (
                RuntimeErrorType.NETWORK
            )

            recoverable = True

        elif isinstance(
            exception,
            ValueError,
        ):

            error_type = (
                RuntimeErrorType.VALIDATION
            )

            recoverable = False

        elif isinstance(
            exception,
            RuntimeError,
        ):

            error_type = (
                RuntimeErrorType.PROVIDER
            )

            recoverable = True

        else:

            error_type = (
                RuntimeErrorType.INTERNAL
            )

            recoverable = False

        return RuntimeErrorInfo(

            error_type=error_type,

            message=str(exception),

            exception_name=name,

            recoverable=recoverable,

            metadata={
                "handled": True,
            },
        )

    def safe_execute(
        self,
        func,
        *args,
        **kwargs,
    ):

        try:

            return (
                True,
                func(
                    *args,
                    **kwargs,
                ),
                None,
            )

        except Exception as exc:

            return (
                False,
                None,
                self.classify(exc),
            )


runtime_error_handler = RuntimeErrorHandler()