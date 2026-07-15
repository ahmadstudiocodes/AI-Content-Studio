# pipelines/telegram_pipeline.py


from datetime import datetime
from uuid import uuid4



class TelegramContentPackage:
    """
    Stores Telegram production package.
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

        self.content = None

        self.summary = None

        self.caption = None

        self.hashtags = None


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

            "content":
                self.content,

            "summary":
                self.summary,

            "caption":
                self.caption,

            "hashtags":
                self.hashtags,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class TelegramPipeline:
    """
    Arman StudioOS

    Professional Telegram Content Pipeline.


    Responsibilities:

    - Telegram content creation
    - Channel post preparation
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


        package = TelegramContentPackage(

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
    # Content Creation
    # =====================================================


    def generate_content(
        self,
        package
    ):


        agent = self.agents.get(
            "article"
        )


        if agent:

            package.content = agent.run(

                package.research or package.topic

            )


        return package



    # =====================================================
    # Summary
    # =====================================================


    def generate_summary(
        self,
        package
    ):


        agent = self.agents.get(
            "summarizer"
        )


        if agent:

            package.summary = agent.run(

                package.content

            )


        return package



    # =====================================================
    # Caption / Hashtag
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


        self.generate_content(

            package

        )


        self.generate_summary(

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

telegram_pipeline = TelegramPipeline()