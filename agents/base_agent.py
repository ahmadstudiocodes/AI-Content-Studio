from abc import ABC, abstractmethod


class BaseAgent(ABC):

    name = "base"

    @abstractmethod
    def can_handle(self, command):
        pass

    @abstractmethod
    def execute(self, command):
        pass

    # برای سازگاری با نسخه‌های قبلی
    def handle(self, command):
        return self.execute(command)