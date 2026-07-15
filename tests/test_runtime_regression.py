import os
import subprocess
import sys


TESTS = [

    "tests/test_context_manager.py",

    "tests/test_execution_pipeline.py",

    "tests/test_provider_executor.py",

    "tests/test_runtime_security.py",

    "tests/test_runtime_recovery.py",

    "tests/test_runtime_gateway.py",

    "tests/test_runtime_lifecycle.py",

    "tests/test_runtime_observability.py",

    "tests/test_runtime_performance.py",

    "tests/test_runtime_full_integration.py",
]


def test_runtime_regression():

    env = os.environ.copy()

    env["PYTHONIOENCODING"] = "utf-8"

    env["PYTHONUTF8"] = "1"


    for test in TESTS:

        result = subprocess.run(
            [
                sys.executable,
                test,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )


        assert (
            result.returncode == 0
        ), (
            f"Failed: {test}\n"
            f"{result.stdout}\n"
            f"{result.stderr}"
        )


if __name__ == "__main__":

    test_runtime_regression()

    print(
        "\n🎉 Runtime Regression Validation Passed"
    )