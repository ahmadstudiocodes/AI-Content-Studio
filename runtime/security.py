from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict


@dataclass(slots=True)
class ValidationResult:
    """
    Result of a security validation.
    """

    allowed: bool

    reason: str = ""


@dataclass(slots=True)
class SecurityPolicy:
    """
    Runtime security policy.
    """

    required_request_fields: tuple[str, ...] = (
        "session_id",
    )

    allowed_providers: set[str] = field(
        default_factory=set,
    )


class RuntimeSecurityValidator:
    """
    Validates runtime requests and providers.
    """

    def __init__(
        self,
        policy: SecurityPolicy | None = None,
    ) -> None:

        self.policy = policy or SecurityPolicy()

    def validate_request(
        self,
        request: Dict[str, Any],
    ) -> ValidationResult:

        if not isinstance(request, dict):

            return ValidationResult(
                False,
                "Request must be a dictionary.",
            )

        for field in self.policy.required_request_fields:

            if field not in request:

                return ValidationResult(
                    False,
                    f"Missing required field: {field}",
                )

        return ValidationResult(True)

    def validate_provider(
        self,
        provider_name: str,
    ) -> ValidationResult:

        if not provider_name:

            return ValidationResult(
                False,
                "Provider name is required.",
            )

        if (
            self.policy.allowed_providers
            and provider_name
            not in self.policy.allowed_providers
        ):

            return ValidationResult(
                False,
                "Provider is not allowed.",
            )

        return ValidationResult(True)

    def validate_context(
        self,
        context: Any,
    ) -> ValidationResult:

        if context is None:

            return ValidationResult(
                False,
                "Runtime context is required.",
            )

        return ValidationResult(True)

    def validate_handler(
        self,
        handler: Callable[..., Any] | None,
    ) -> ValidationResult:

        if handler is None:

            return ValidationResult(
                False,
                "Handler is required.",
            )

        if not callable(handler):

            return ValidationResult(
                False,
                "Handler must be callable.",
            )

        return ValidationResult(True)

    def validate_providers(
        self,
        providers: Dict[str, Callable[..., Any]] | None,
    ) -> ValidationResult:

        if providers is None:

            return ValidationResult(
                False,
                "Providers collection is required.",
            )

        if not isinstance(providers, dict):

            return ValidationResult(
                False,
                "Providers must be a dictionary.",
            )

        if len(providers) == 0:

            return ValidationResult(
                False,
                "At least one provider is required.",
            )

        for name, handler in providers.items():

            result = self.validate_provider(
                name,
            )

            if not result.allowed:

                return result

            result = self.validate_handler(
                handler,
            )

            if not result.allowed:

                return result

        return ValidationResult(True)


runtime_security_validator = (
    RuntimeSecurityValidator()
)