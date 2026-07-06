from core.command import Command


class CommandParser:

    def parse(self, text):

        return Command(text)


parser = CommandParser()