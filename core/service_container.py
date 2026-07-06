class ServiceContainer:

    def __init__(self):

        self.services = {}

    def register(self, name, service):

        self.services[name] = service

    def resolve(self, name):

        return self.services.get(name)


container = ServiceContainer()