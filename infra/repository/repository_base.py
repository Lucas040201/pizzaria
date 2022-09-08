from abc import ABC
from app.infra.configs.connection import DBConnectionHandler
from app import db as app_db


class RepositoryBase(ABC):
    def __init__(self, model):
        self.__model = model
        self.__handler = DBConnectionHandler
        self.__db = app_db

    def create_handler(self):
        return self.__handler(self.__db)

    def model(self):
        return self.__model

    def list(self):
        with self.create_handler() as db:
            data = db.session.query(self.__model).all()
        return data

    def insert(self, data):
        with self.create_handler() as db:
            try:
                print(self.__model(**data))
                instance = self.__model(**data)
                db.session.add(instance)
                db.session.commit()

                return instance
            except:
                db.session.rollback()

    def delete(self, instance_id):
        with self.create_handler() as db:
            try:
                deleted = db.session.query(self.__model).filter(self.__model.id == instance_id).delete()
                db.session.commit()
                return deleted
            except:
                db.session.rollback()

    def update(self, instance_id, data):
        with self.create_handler() as db:
            try:
                instance = db.session.query(self.__model).filter(self.__model.id == instance_id).update(data)
                db.session.commit()
                return instance
            except:
                db.session.rollback()

    def show(self, instance_id):
        with self.create_handler() as db:
            try:
                data = db.session.query(self.__model).filter(self.__model.id == instance_id).first()
                return data
            except:
                db.session.rollback()
