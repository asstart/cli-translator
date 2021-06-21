from repository import InitRepository


class InitController:

    def __init__(self, init_repository: InitRepository):
        self.repository = init_repository
        self.init_db()

    def init_session(self) -> str:
        return self.repository.init_session()

    def init_db(self):
        self.repository.init_translations_db()