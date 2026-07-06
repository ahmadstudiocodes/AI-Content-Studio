class ProviderManager:

    def __init__(self):

        self.providers = {}

    def register(self, provider):

        self.providers[provider.name] = provider

    def get(self, name):

        return self.providers.get(name)

    def default(self):

        for provider in self.providers.values():

            if provider.available():

                return provider

        return None


provider_manager = ProviderManager()