from memory.service import memory_service


def search(text):

    return memory_service.recall(text)