import traceback

from brain.controller import controller

from core.output_cleaner import OutputCleaner
from core.validator import Validator
from core.quality_evaluator import QualityEvaluator
from core.retry_engine import retry_engine


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
    Quality
        ↓
    Retry
        ↓
    Success
    """

    def __init__(self):

        self.validator = Validator()
        self.quality = QualityEvaluator()

    def execute(
        self,
        command
    ):

        command.plan.status = "running"

        try:

            # ----------------------------------
            # Worker
            # ----------------------------------

            def worker():

                result = controller.execute(
                    command
                )

                cleaned = OutputCleaner.clean(
                    result
                )

                return cleaned

            # ----------------------------------
            # Retry Engine
            # ----------------------------------

            retry_result = retry_engine.execute(

                worker=worker,

                validator=self.validator,

                task=command.action,

                topic=command.payload or ""

            )

            cleaned = retry_result["output"]

            validation = retry_result["validation"]

            # ----------------------------------
            # Quality Evaluation
            # ----------------------------------

            quality = self.quality.evaluate(
                cleaned
            )

            # ----------------------------------
            # Retry Required
            # ----------------------------------

            if validation.get("retry"):

                command.plan.status = "retry_required"

                return {

                    "output": cleaned,

                    "validation": validation,

                    "quality": quality,

                    "status": "retry_required"

                }

            if quality.get("retry"):

                command.plan.status = "retry_required"

                return {

                    "output": cleaned,

                    "validation": validation,

                    "quality": quality,

                    "status": "retry_required"

                }

            # ----------------------------------
            # Success
            # ----------------------------------

            command.plan.complete()

            return {

                "output": cleaned,

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