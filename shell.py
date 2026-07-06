from core.dispatcher import dispatcher


class Shell:

    def start(self):

        print()

        while True:

            try:

                command = input("Arman> ").strip()

                if command == "":
                    continue

                if command.lower() in ["exit", "quit"]:

                    print("Goodbye Ahmad 👋")
                    break

                response = dispatcher.route(command)

                if response:
                    print(response)

            except KeyboardInterrupt:

                print()
                print("Goodbye Ahmad 👋")
                break