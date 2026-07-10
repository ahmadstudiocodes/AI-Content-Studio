from core.command import Command


class CommandParser:

    """
    Converts raw user input into a Command object.
    """

    def parse(self, text):

        if text is None:
            text = ""

        text = str(text).strip()

        return Command(text)


parser = CommandParser()