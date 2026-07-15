import traceback

from brain.controller import controller

from core.output_cleaner import OutputCleaner
from core.validator import Validator
from core.quality_evaluator import quality_evaluator


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
    Quality Evaluator
        ↓
    Retry / Success
    """

    def __init__(self):

        self.validator = Validator()


    def execute(
        self,
        command
    ):

        if command.plan:

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
            # Validator
            # ----------------------------------

            validation = self.validator.validate(

                cleaned,

                command.action,

                command.payload

            )


            if validation.get("retry"):

                if command.plan:

                    command.plan.status = "retry_required"


                return {

                    "output": cleaned,

                    "validation": validation,

                    "quality": None,

                    "status": "retry_required"

                }



            # ----------------------------------
            # Determine Agent Type
            # ----------------------------------

            agent_type = (

                getattr(

                    command,

                    "target",

                    ""

                )

                or ""

            ).lower()



            if not agent_type:

                agent_type = (

                    getattr(

                        command,

                        "action",

                        ""

                    )

                    or ""

                ).lower()



            # ----------------------------------
            # Quality Evaluation
            # ----------------------------------

            quality = quality_evaluator.evaluate(

                cleaned,

                agent_type,

                command.payload

            )


            if quality.get("retry"):

                if command.plan:

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

            if command.plan:

                command.plan.complete()


            return {

                "output": cleaned,

                "validation": validation,

                "quality": quality,

                "status": "completed"

            }



        except Exception as e:


            traceback.print_exc()


            if command.plan:

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

                "quality": None,

                "status": "failed"

            }



pipeline = ExecutionPipeline()