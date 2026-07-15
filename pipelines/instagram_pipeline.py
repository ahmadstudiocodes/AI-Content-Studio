# pipelines/instagram_pipeline.py


from datetime import datetime
from uuid import uuid4



class InstagramContentPackage:
    """
    Stores Instagram content package.
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

        self.caption = None

        self.visual = None

        self.hashtags = None

        self.short_video = None


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

            "caption":
                self.caption,

            "visual":
                self.visual,

            "hashtags":
                self.hashtags,

            "short_video":
                self.short_video,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class InstagramPipeline:
    """
    Arman StudioOS

    Professional Instagram Content Pipeline.


    Responsibilities:

    - Instagram workflow
    - Content packaging
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


        package = InstagramContentPackage(

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
    # Caption
    # =====================================================


    def generate_caption(
        self,
        package
    ):


        agent = self.agents.get(
            "script"
        )


        if agent:

            package.caption = agent.run(

                package.topic

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
    # Hashtag / SEO
    # =====================================================


    def generate_hashtags(
        self,
        package
    ):


        agent = self.agents.get(
            "seo"
        )


        if agent:

            package.hashtags = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Full Pipeline
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


        self.generate_caption(

            package

        )


        self.generate_visual(

            package

        )


        self.generate_hashtags(

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

instagram_pipeline = InstagramPipeline()