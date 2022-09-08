from abc import ABC


class ServiceBase(ABC):
    def __init__(self, repository):
        self.__repository = repository

    def repository(self):
        return self.__repository

    def list(self):
        return self.__repository.list()

    def insert(self, data):
        return self.__repository.insert(data)

    def delete(self, instance_id):
        return self.__repository.delete(instance_id)

    def update(self, instance, data):
        return self.__repository.update(instance, data)

    def show(self, instance_id):
        return self.__repository.show(instance_id)