class RetryEngine:
    """
    Retry Engine for Arman StudioOS

    Executes worker repeatedly until the output
    passes validation or retries are exhausted.
    """

    def __init__(
        self,
        max_retries=2
    ):

        self.max_retries = max_retries

    def execute(
        self,
        worker,
        validator,
        task="",
        topic="",
        retry_builder=None
    ):

        attempt = 0

        last_output = ""

        last_validation = {

            "valid": False,

            "retry": True,

            "reason": "UNKNOWN",

            "errors": []

        }

        while attempt <= self.max_retries:

            attempt += 1

            try:

                output = worker()

            except Exception as e:

                last_output = ""

                last_validation = {

                    "valid": False,

                    "retry": attempt <= self.max_retries,

                    "reason": "WORKER_EXCEPTION",

                    "errors": [

                        str(e)

                    ]

                }

                if not last_validation["retry"]:

                    break

                continue

            last_output = output

            last_validation = validator.validate(

                output=output,

                task=task,

                topic=topic

            )

            print(
                f"[RETRY] Attempt {attempt}/{self.max_retries + 1}"
            )

            print(
                f"[RETRY] Result: {last_validation['reason']}"
            )

            if last_validation["valid"]:

                return {

                    "success": True,

                    "attempt": attempt,

                    "output": output,

                    "validation": last_validation

                }

            if not last_validation.get(
                "retry",
                True
            ):

                break

        return {

            "success": False,

            "attempt": attempt,

            "output": last_output,

            "validation": last_validation

        }


retry_engine = RetryEngine()