class History:

    def __init__(self):

        self.items = []

    def add(self, role, text):

        self.items.append(

            {
                "role": role,
                "text": text
            }

        )

    def last(self, count=10):

        return self.items[-count:]


history = History()