import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.security import (
    RuntimeSecurityValidator,
    SecurityPolicy,
    runtime_security_validator,
)

from runtime.provider_executor import (
    RuntimeProviderExecutor,
)

from runtime.context import (
    RuntimeContext,
)


def test_request_validation():

    validator = RuntimeSecurityValidator()

    result = validator.validate_request(
        {
            "session_id": "abc",
        }
    )

    assert result.allowed


def test_request_missing_field():

    validator = RuntimeSecurityValidator()

    result = validator.validate_request({})

    assert result.allowed is False


def test_provider_validation():

    validator = RuntimeSecurityValidator(
        SecurityPolicy(
            allowed_providers={
                "ollama",
                "openai",
            }
        )
    )

    assert validator.validate_provider(
        "ollama"
    ).allowed

    assert (
        validator.validate_provider(
            "gemini"
        ).allowed
        is False
    )


def test_provider_filtering():

    runtime_security_validator.policy = SecurityPolicy(
        allowed_providers={
            "backup",
        }
    )

    executor = RuntimeProviderExecutor()

    context = RuntimeContext()

    providers = {
        "primary": lambda: "primary-result",
        "backup": lambda: "backup-result",
    }

    result = executor.execute(
        context,
        providers,
    )

    assert result.success

    assert result.provider == "backup"

    assert result.data == "backup-result"


if __name__ == "__main__":

    test_request_validation()
    test_request_missing_field()
    test_provider_validation()
    test_provider_filtering()

    print(
        "\n🎉 Runtime Security Validation Passed"
    )