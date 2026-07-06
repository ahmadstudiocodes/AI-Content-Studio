class ThumbnailAgent:

    def create(self, title):

        return {
            "title": title,
            "prompt": "",
            "status": "waiting"
        }


thumbnail_agent = ThumbnailAgent()