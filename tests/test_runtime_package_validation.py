import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT),
    )


REQUIRED_MODULES = [

    "runtime.context",

    "runtime.context_manager",

    "runtime.execution_pipeline",

    "runtime.provider_executor",

    "runtime.lifecycle",

    "runtime.security",

    "runtime.recovery",

    "runtime.retry",

    "runtime.failover",

    "runtime.api_gateway",

    "runtime.observability",

    "runtime.performance",

    "runtime.diagnostics",

]


def test_runtime_package_validation():

    for module_name in REQUIRED_MODULES:

        module = __import__(
            module_name,
            fromlist=["*"],
        )

        assert module is not None


if __name__ == "__main__":

    test_runtime_package_validation()

    print(
        "\n🎉 Runtime Package Validation Passed"
    )