import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


from runtime.api_gateway import (
    RuntimeAPIGateway,
)



def test_gateway_success():


    gateway = RuntimeAPIGateway()


    providers = {

        "main":
            lambda: "response"

    }


    response = gateway.handle(

        {
            "session_id":
                "session-test"
        },

        providers
    )


    assert response.success

    assert (
        response.data
        ==
        "response"
    )

    assert response.trace_id



def test_gateway_invalid_request():


    gateway = RuntimeAPIGateway()


    response = gateway.handle(
        None,
        {}
    )


    assert response.success is False



if __name__ == "__main__":


    test_gateway_success()

    test_gateway_invalid_request()


    print(
        "\n🎉 Runtime Gateway Validation Passed"
    )