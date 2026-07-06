from collections import defaultdict


class EventBus:

    def __init__(self):

        self.listeners = defaultdict(list)

    def subscribe(self, event, callback):

        self.listeners[event].append(callback)

    def emit(self, event, data=None):

        if event not in self.listeners:
            return

        for callback in self.listeners[event]:
            callback(data)


event_bus = EventBus()