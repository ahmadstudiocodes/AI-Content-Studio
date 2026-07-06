class Workflow:

    def __init__(self,name):

        self.name=name

        self.steps=[]

    def add_step(self,step):

        self.steps.append(step)

    def execute(self):

        for step in self.steps:

            step()

