import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.failover import (
    FailoverPolicy,
    ProviderFailover,
)



def main():

    print("\n=== Provider Failover Test ===")


    policy = FailoverPolicy(
        providers=[
            "openai",
            "gemini",
            "ollama",
        ],
        max_retries=2,
    )


    failover = ProviderFailover(
        policy
    )


    fallback = (
        failover.next_provider(
            "openai"
        )
    )


    print(
        "Fallback:",
        fallback,
    )


    assert (
        fallback == "gemini"
    )


    failover.record_failure(
        "openai"
    )


    failover.record_failure(
        "openai"
    )


    print(
        "Failures:",
        failover.health(),
    )


    print(
        "\n🎉 Provider Failover Validation Passed"
    )



if __name__ == "__main__":
    main()