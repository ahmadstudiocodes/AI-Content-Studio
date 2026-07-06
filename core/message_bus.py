from queue import Queue


class MessageBus:

    def __init__(self):

        self.queue = Queue()

    def send(self, message):

        self.queue.put(message)

    def receive(self):

        if self.queue.empty():

            return None

        return self.queue.get()


message_bus = MessageBus()