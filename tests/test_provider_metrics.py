import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.metrics import provider_metrics



def main():

    print("\n=== Provider Metrics Test ===")


    provider_metrics.clear()


    provider_metrics.record_success(
        "ollama",
        0.25,
    )


    provider_metrics.record_success(
        "ollama",
        0.35,
    )


    provider_metrics.record_failure(
        "openai",
        1.2,
    )


    report = provider_metrics.all()


    print(
        "Metrics:"
    )

    print(
        report
    )


    assert (
        report["ollama"]["requests"]
        == 2
    )

    assert (
        report["ollama"]["successes"]
        == 2
    )


    print(
        "\n🎉 Provider Metrics Validation Passed"
    )



if __name__ == "__main__":
    main()