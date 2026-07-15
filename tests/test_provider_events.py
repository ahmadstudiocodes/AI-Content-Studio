import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


from providers.events import (
    ProviderEvent,
    provider_event_bus,
)



def main():

    print("\n=== Provider Events Test ===")


    provider_event_bus.clear()


    provider_event_bus.emit(
        ProviderEvent(
            name="provider.loaded",
            provider="ollama",
            data={
                "model": "qwen3:4b"
            },
        )
    )


    provider_event_bus.emit(
        ProviderEvent(
            name="provider.request.completed",
            provider="ollama",
            data={
                "latency": 0.25
            },
        )
    )


    events = (
        provider_event_bus.history()
    )


    print(
        "Events:"
    )

    for event in events:
        print(
            event
        )


    assert len(events) == 2


    assert (
        events[0].name
        ==
        "provider.loaded"
    )


    print(
        "\n🎉 Provider Events Validation Passed"
    )


if __name__ == "__main__":
    main()