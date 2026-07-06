from brain.reasoning import reasoning


class CommandProcessor:

    def process(self, command):

        return reasoning.think(command)


processor = CommandProcessor()