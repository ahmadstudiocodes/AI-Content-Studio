class VideoAgent:

    def render(self, project):

        return {
            "project": project,
            "status": "rendering"
        }


video_agent = VideoAgent()