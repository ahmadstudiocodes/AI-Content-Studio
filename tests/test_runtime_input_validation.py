import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.security import (
    runtime_security_validator,
)


def test_context_validation():

    assert not (
        runtime_security_validator
        .validate_context(None)
        .allowed
    )

    assert (
        runtime_security_validator
        .validate_context(object())
        .allowed
    )


def test_handler_validation():

    assert (
        runtime_security_validator
        .validate_handler(lambda: None)
        .allowed
    )

    assert not (
        runtime_security_validator
        .validate_handler(None)
        .allowed
    )

    assert not (
        runtime_security_validator
        .validate_handler("not_callable")
        .allowed
    )


def test_provider_collection_validation():

    assert not (
        runtime_security_validator
        .validate_providers({})
        .allowed
    )

    assert (
        runtime_security_validator
        .validate_providers(
            {
                "demo": lambda: "ok",
            }
        ).allowed
    )


if __name__ == "__main__":

    test_context_validation()

    test_handler_validation()

    test_provider_collection_validation()

    print(
        "\n🎉 Runtime Input Validation Passed"
    )