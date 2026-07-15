class AgentRegistry:

    """
    Arman StudioOS Agent Registry

    Responsible for:

    - Registering agents
    - Finding agents
    - Managing agent lifecycle

    """


    def __init__(
        self
    ):

        self._agents = {}



    # ==================================================

    def register(
        self,
        name,
        agent
    ):


        if not name:

            raise ValueError(
                "Agent name is required"
            )


        if agent is None:

            raise ValueError(
                "Agent instance is required"
            )


        key = str(
            name
        ).lower()



        self._agents[key] = agent



        return True



    # ==================================================

    def unregister(
        self,
        name
    ):


        if not name:

            return False



        return self._agents.pop(

            str(name).lower(),

            None

        ) is not None



    # ==================================================

    def get(
        self,
        name
    ):


        if not name:

            return None



        return self._agents.get(

            str(name).lower()

        )



    # ==================================================

    def exists(
        self,
        name
    ):


        if not name:

            return False



        return (

            str(name).lower()

            in self._agents

        )



    # ==================================================

    def all(
        self
    ):


        return dict(
            self._agents
        )



    # ==================================================

    def count(
        self
    ):


        return len(
            self._agents
        )



    # ==================================================

    def clear(
        self
    ):


        self._agents.clear()



registry = AgentRegistry()