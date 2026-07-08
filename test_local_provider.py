from providers.local_provider import LocalProvider

provider = LocalProvider()

print("Provider Available:", provider.available())

response = provider.generate("سلام، خودت را معرفی کن.")

print("\nResponse:\n")
print(response)