# pipelines/tiktok_pipeline.py


from datetime import datetime
from uuid import uuid4



class TikTokContentPackage:
    """
    Stores TikTok production package.
    """

    def __init__(
        self,
        topic
    ):

        self.id = str(
            uuid4()
        )

        self.topic = topic


        self.research = None

        self.hook = None

        self.script = None

        self.video_plan = None

        self.visual = None

        self.caption = None


        self.status = "created"


        self.created_at = datetime.utcnow()



    def to_dict(
        self
    ):

        return {

            "id":
                self.id,

            "topic":
                self.topic,

            "research":
                self.research,

            "hook":
                self.hook,

            "script":
                self.script,

            "video_plan":
                self.video_plan,

            "visual":
                self.visual,

            "caption":
                self.caption,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class TikTokPipeline:
    """
    Arman StudioOS

    Professional TikTok Production Pipeline.


    Responsibilities:

    - Short form content workflow
    - Viral structure planning
    - Agent coordination
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        agents=None
    ):

        self.agents = agents or {}

        self.projects = {}



    # =====================================================
    # Create
    # =====================================================


    def create(
        self,
        topic
    ):


        package = TikTokContentPackage(

            topic

        )


        self.projects[package.id] = package


        return package



    # =====================================================
    # Research
    # =====================================================


    def run_research(
        self,
        package
    ):


        agent = self.agents.get(
            "research"
        )


        if agent:

            package.research = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Hook & Script
    # =====================================================


    def generate_script(
        self,
        package
    ):


        agent = self.agents.get(
            "script"
        )


        if agent:

            package.script = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Video Planning
    # =====================================================


    def generate_video_plan(
        self,
        package
    ):


        agent = self.agents.get(
            "video_planner"
        )


        if agent:

            package.video_plan = agent.run(

                package.script or package.topic

            )


        return package



    # =====================================================
    # Visual
    # =====================================================


    def generate_visual(
        self,
        package
    ):


        agent = self.agents.get(
            "image"
        )


        if agent:

            package.visual = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Caption
    # =====================================================


    def generate_caption(
        self,
        package
    ):


        agent = self.agents.get(
            "seo"
        )


        if agent:

            package.caption = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Execute
    # =====================================================


    def execute(
        self,
        topic
    ):


        package = self.create(

            topic

        )


        self.run_research(

            package

        )


        self.generate_script(

            package

        )


        self.generate_video_plan(

            package

        )


        self.generate_visual(

            package

        )


        self.generate_caption(

            package

        )


        package.status = "completed"


        return package



    # =====================================================
    # Query
    # =====================================================


    def get(
        self,
        project_id
    ):


        package = self.projects.get(

            project_id

        )


        if package:

            return package.to_dict()


        return None



# Global Instance

tiktok_pipeline = TikTokPipeline()