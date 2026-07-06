from queue import Queue


class TaskQueue:

    def __init__(self):

        self.queue = Queue()

    def push(self, task):

        self.queue.put(task)

    def pop(self):

        if self.queue.empty():

            return None

        return self.queue.get()

    def size(self):

        return self.queue.qsize()


task_queue = TaskQueue()