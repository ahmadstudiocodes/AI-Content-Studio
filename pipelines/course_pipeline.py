# pipelines/course_pipeline.py


from datetime import datetime
from uuid import uuid4



class CourseContentPackage:
    """
    Stores complete course production package.
    """

    def __init__(
        self,
        topic
    ):

        self.id = str(
            uuid4()
        )

        self.topic = topic


        self.structure = None

        self.lessons = []

        self.scripts = []

        self.voice = []


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

            "structure":
                self.structure,

            "lessons":
                self.lessons,

            "scripts":
                self.scripts,

            "voice":
                self.voice,

            "status":
                self.status,

            "created_at":
                self.created_at.isoformat()

        }





class CoursePipeline:
    """
    Arman StudioOS

    Professional Course Production Pipeline.


    Responsibilities:

    - Course creation workflow
    - Lesson generation
    - Educational packaging
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        agents=None
    ):

        self.agents = agents or {}

        self.projects = {}



    # =====================================================
    # Create Course
    # =====================================================


    def create(
        self,
        topic
    ):


        package = CourseContentPackage(

            topic

        )


        self.projects[package.id] = package


        return package



    # =====================================================
    # Course Structure
    # =====================================================


    def build_structure(
        self,
        package
    ):


        agent = self.agents.get(
            "course"
        )


        if agent:

            package.structure = agent.run(

                package.topic

            )


        return package



    # =====================================================
    # Lesson Scripts
    # =====================================================


    def generate_lessons(
        self,
        package
    ):


        script_agent = self.agents.get(
            "script"
        )


        if script_agent and package.structure:


            result = script_agent.run(

                package.structure

            )


            package.scripts.append(

                result

            )


        return package



    # =====================================================
    # Voice Preparation
    # =====================================================


    def generate_voice(
        self,
        package
    ):


        voice_agent = self.agents.get(
            "voice"
        )


        if voice_agent and package.scripts:


            for script in package.scripts:


                package.voice.append(

                    voice_agent.run(
                        script
                    )

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


        self.build_structure(

            package

        )


        self.generate_lessons(

            package

        )


        self.generate_voice(

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

course_pipeline = CoursePipeline()