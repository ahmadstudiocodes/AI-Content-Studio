from core.task import Task


class TaskBuilder:

    def build(self, command):

        task = Task()

        task.action = command.action

        task.domain = command.intent.domain

        task.target = command.target

        task.arguments = command.args

        # Sprint 9
        task.payload = command.payload

        task.priority = command.intent.priority

        task.provider = command.intent.provider

        task.need_memory = command.intent.need_memory

        return task


task_builder = TaskBuilder()