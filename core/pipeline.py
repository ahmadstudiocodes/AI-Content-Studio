import traceback

from brain.controller import controller

from core.validator import validator
from core.quality_evaluator import quality_evaluator
from core.retry_engine import retry_engine


class ExecutionPipeline:
    """
    Main Execution Pipeline

    Command
        ↓
    Brain
        ↓
    Validator
        ↓
    Quality
        ↓
    Retry
        ↓
    Success
    """

    def __init__(self):

        self.validator = validator
        self.quality = quality_evaluator

    def execute(self, command):

        command.plan.status = "running"

        try:

            def worker():

                return controller.execute(command)

            retry_result = retry_engine.execute(

                worker=worker,

                validator=self.validator,

                task=command.action,

                topic=command.payload or ""

            )

            output = retry_result["output"]

            validation = retry_result["validation"]

            quality = self.quality.evaluate(

                output=output,

                task=command.action,

                topic=command.payload or ""

            )

            if validation["retry"]:

                command.plan.status = "retry_required"

                return {

                    "output": output,

                    "validation": validation,

                    "quality": quality,

                    "status": "retry_required"

                }

            if quality["retry"]:

                command.plan.status = "retry_required"

                return {

                    "output": output,

                    "validation": validation,

                    "quality": quality,

                    "status": "retry_required"

                }

            command.plan.complete()

            return {

                "output": output,

                "validation": validation,

                "quality": quality,

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

                "quality": {

                    "score": 0,

                    "passed": False,

                    "retry": True,

                    "issues": [

                        str(e)

                    ]

                },

                "status": "failed"

            }


pipeline = ExecutionPipeline()