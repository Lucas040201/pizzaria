from abc import ABC


class ServiceBase(ABC):
    def __init__(self, repository):
        self.__repository = repository

    def repository(self):
        return self.__repository

    def list(self):
        return self.__repository.list()

    def insert(self, data: {}):
        return self.__repository.insert(data)

    def delete(self, instance_id: int):
        return self.__repository.delete(instance_id)

    def update(self, instance_id: int, data: {}):
        return self.__repository.update(instance_id, data)

    def show(self, instance_id: int):
        return self.__repository.show(instance_id)