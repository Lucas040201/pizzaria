class DBConnectionHandler:

    def __init__(self, db) -> None:
        self.__db = db
        self.session = None

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = self.__db.session
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.expunge_all()
        self.session.close()
