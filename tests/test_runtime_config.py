import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.config import (
    RuntimeConfigManager,
)

from runtime.environment import (
    RuntimeEnvironment,
    EnvironmentManager,
)



def test_config_features():


    manager = RuntimeConfigManager()


    manager.set_feature(
        "ai_runtime",
        True
    )


    assert (
        manager.is_enabled(
            "ai_runtime"
        )
        is True
    )



def test_provider_config():


    manager = RuntimeConfigManager()


    manager.set_provider(
        "ollama",
        {
            "model": "qwen"
        }
    )


    assert (
        manager.config.providers["ollama"]["model"]
        ==
        "qwen"
    )



def test_environment():


    env = EnvironmentManager(
        RuntimeEnvironment.TESTING
    )


    assert (
        env.current()
        ==
        "testing"
    )



def test_validation():


    manager = RuntimeConfigManager()


    assert (
        manager.validate()
        is True
    )



if __name__ == "__main__":

    test_config_features()

    test_provider_config()

    test_environment()

    test_validation()


    print(
        "\n🎉 Runtime Configuration Validation Passed"
    )