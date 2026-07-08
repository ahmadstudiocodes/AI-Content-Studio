from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name = "base"

    version = "1.0"

    description = "Base Agent"

    supported_commands = []

    @abstractmethod
    def can_handle(self, command):
        pass

    @abstractmethod
    def execute(self, command):
        pass

    # سازگاری با نسخه‌های قبلی
    def handle(self, command):
        return self.execute(command)

    # اطلاعات Agent
    def info(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "supported_commands": self.supported_commands,
        }