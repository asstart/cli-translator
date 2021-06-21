from repository import ExportRepository
from csvwriter import CsvWriter

class ExportController:

    def __init__(self, repository: ExportRepository, writer: CsvWriter):
        self.repository = repository

    def export_by_session(self, session_id: str):
        data = self.repository.get_all_by_session(session_id)
        if data:
            for json in data:
                pass


    def export_all(self):
        pass
