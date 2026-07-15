from agents.base.base_llm_agent import BaseLLMAgent



class CourseAgent(BaseLLMAgent):
    """
    Arman StudioOS

    Professional Course Design Agent


    Responsibilities:

    - Course architecture
    - Lesson planning
    - Learning path
    - Exercises
    - Educational structure
    """



    VERSION = "1.0.0"



    def __init__(
        self,
        provider
    ):


        super().__init__(

            name="course",

            description=
            "Professional Course Creation Agent",

            provider=provider,

            system_prompt="""

You are Arman StudioOS Course Agent.

Your responsibility is designing educational courses.

Focus on:

- Learning objectives
- Course structure
- Lessons
- Exercises
- Projects
- Student progression


Never:

- Write marketing content
- Generate thumbnails
- Perform SEO optimization

"""

        )



        self.priority = 80



        self.domains = [

            "education",

            "course",

            "training"

        ]



        self.capabilities = [

            "course_design",

            "lesson_planning",

            "learning_path",

            "exercise_creation"

        ]



    # =====================================================
    # Capability
    # =====================================================


    def has_capability(
        self,
        capability
    ):

        return capability in self.capabilities



    # =====================================================
    # Dispatcher
    # =====================================================


    def can_handle(
        self,
        user_input
    ):


        text = str(
            user_input
        ).lower()



        keywords = [

            "course",

            "دوره",

            "آموزش",

            "درس",

            "فصل",

            "تمرین",

            "کلاس"

        ]



        return any(

            key in text

            for key in keywords

        )



    # =====================================================
    # Prompt Builder
    # =====================================================


    def build_prompt(
        self,
        user_input
    ):


        return f"""

{self.system_prompt}


USER REQUEST:

{user_input}



Required Structure:


# Course Overview


# Target Students


# Learning Objectives


# Course Modules


# Lessons Breakdown


# Exercises


# Final Project


# Learning Path



Rules:

- Answer in Persian.
- Create practical educational structures.
- Consider student progression.

"""



    # =====================================================
    # Post Processing
    # =====================================================


    def postprocess(
        self,
        response,
        user_input=None
    ):


        return super().postprocess(
            response,
            user_input
        )