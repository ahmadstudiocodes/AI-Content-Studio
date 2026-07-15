# pipelines/blog_pipeline.py


from datetime import datetime
from uuid import uuid4



class BlogContentPackage:
    """
    Stores complete blog production package.
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

        self.article = None

        self.seo = None

        self.translation = None


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

            "article":
                self.article,

            "seo":
                self.seo,

            "translation":
                self.translation,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class BlogPipeline:
    """
    Arman StudioOS

    Professional Blog Production Pipeline.


    Responsibilities:

    - Article workflow
    - Agent coordination
    - Content packaging
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


        package = BlogContentPackage(

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
    # Article
    # =====================================================


    def run_article(
        self,
        package
    ):


        agent = self.agents.get(
            "article"
        )


        if agent:

            package.article = agent.run(

                package.research or package.topic

            )


        return package



    # =====================================================
    # SEO
    # =====================================================


    def run_seo(
        self,
        package
    ):


        agent = self.agents.get(
            "seo"
        )


        if agent:

            package.seo = agent.run(

                package.article or package.topic

            )


        return package



    # =====================================================
    # Translation
    # =====================================================


    def run_translation(
        self,
        package
    ):


        agent = self.agents.get(
            "translation"
        )


        if agent:

            package.translation = agent.run(

                package.article

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


        self.run_article(
            package
        )


        self.run_seo(
            package
        )


        self.run_translation(
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

blog_pipeline = BlogPipeline()