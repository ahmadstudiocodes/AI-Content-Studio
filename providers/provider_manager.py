class ProviderManager:

    def __init__(self):

        self.providers = {}

    def register(self, provider):

        self.providers[provider.name] = provider

    def get(self, name):

        return self.providers.get(name)

    def default(self):

        print("\n========== PROVIDERS ==========")

        for name, provider in self.providers.items():

            status = provider.available()

            print(
                f"{name:<10} -> {'ONLINE' if status else 'OFFLINE'}"
            )

            if status:

                print("===============================\n")

                return provider

        print("===============================\n")

        return None


provider_manager = ProviderManager()