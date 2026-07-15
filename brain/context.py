class Context:
    """
    Shared Brain Context

    Stores temporary workflow data that
    can be shared between Brain modules.
    """

    def __init__(self):

        self.data = {}

    # ---------------------------------

    def set(
        self,
        key,
        value
    ):

        self.data[key] = value

    # ---------------------------------

    def get(
        self,
        key,
        default=None
    ):

        return self.data.get(
            key,
            default
        )

    # ---------------------------------

    def has(
        self,
        key
    ):

        return key in self.data

    # ---------------------------------

    def remove(
        self,
        key
    ):

        if key in self.data:

            del self.data[key]

    # ---------------------------------

    def update(
        self,
        values
    ):

        if isinstance(
            values,
            dict
        ):

            self.data.update(
                values
            )

    # ---------------------------------

    def clear(self):

        self.data.clear()

    # ---------------------------------

    def snapshot(self):

        return dict(
            self.data
        )

    # ---------------------------------

    def __contains__(
        self,
        key
    ):

        return key in self.data

    # ---------------------------------

    def __len__(self):

        return len(
            self.data
        )

    # ---------------------------------

    def __str__(self):

        return (
            f"Context(keys={list(self.data.keys())})"
        )


context = Context()