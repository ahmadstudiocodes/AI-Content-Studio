import traceback

from brain.controller import controller

from core.output_cleaner import OutputCleaner

from core.validator import Validator


class ExecutionPipeline:

    """
    Main Execution Pipeline

    Command
        ↓
    Brain
        ↓
    Cleaner
        ↓
    Validator
        ↓
    Retry / Success
    """

    def __init__(self):

        self.validator = Validator()

    def execute(
        self,
        command
    ):

        command.plan.status = "running"

        try:

            # ----------------------------------
            # Brain
            # ----------------------------------

            result = controller.execute(
                command
            )

            # ----------------------------------
            # Clean Output
            # ----------------------------------

            cleaned = OutputCleaner.clean(
                result
            )

            # ----------------------------------
            # Validate
            # ----------------------------------

            validation = self.validator.validate(

                cleaned,

                command.action,

                command.payload

            )

            # ----------------------------------
            # Retry
            # ----------------------------------

            if validation.get("retry"):

                command.plan.status = "retry_required"

                return {

                    "output": cleaned,

                    "validation": validation,

                    "status": "retry_required"

                }

            # ----------------------------------
            # Success
            # ----------------------------------

            command.plan.complete()

            return {

                "output": cleaned,

                "validation": validation,

                "status": "completed"

            }

        except Exception as e:

            traceback.print_exc()

            command.plan.status = "failed"

            return {

                "output": "",

                "validation": {

                    "valid": False,

                    "retry": True,

                    "reason": "PIPELINE_ERROR",

                    "errors": [

                        str(e)

                    ]

                },

                "status": "failed"

            }


pipeline = ExecutionPipeline()