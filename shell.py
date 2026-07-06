from core.parser import parser
from core.intent_engine import intent_engine
from core.task_builder import task_builder
from core.planner import planner
from core.execution_pipeline import pipeline


class Shell:

    def start(self):

        print()

        while True:

            try:

                text = input("Arman> ").strip()

                if not text:
                    continue

                if text.lower() in ["exit", "quit"]:

                    print("Goodbye Ahmad 👋")

                    break

                command = parser.parse(text)

                command.intent = intent_engine.analyze(command)

                command.task = task_builder.build(command)

                command.plan = planner.create(command.task)

                response = pipeline.execute(command)

                if response:

                    print(response)

            except KeyboardInterrupt:

                print()

                print("Goodbye Ahmad 👋")

                break