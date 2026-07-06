class PublisherAgent:

    def upload(self, platform):

        return {
            "platform": platform,
            "status": "waiting"
        }


publisher_agent = PublisherAgent()