from translator.export.repository import ExportRepository
from translator.model import tr_to_translations
from translator.export.csvwriter import CsvWriter


class ExportController:

    def __init__(self, repository: ExportRepository, writer: CsvWriter):
        self.repository = repository
        self.writer = writer

    def export_by_session(self, session_id: str):
        if not self.is_session_valid(session_id):
            raise Exception(f"Session: {session_id} not found".format(session_id=session_id))

        data = self.repository.get_all_by_session(session_id)
        translations = self._to_translations(data)
        if len(translations) > 0:
            self.writer.make_file(translations)

    def is_session_valid(self, session) -> bool:
        return session is not None and session

    def export_all(self):
        data = self.repository.get_all()
        translations = self._to_translations(data)
        if len(translations) > 0:
            self.writer.make_file(translations)

    def _to_translations(self, data):
        translations = []
        if data:
            for tr in data:
                translations.extend(tr_to_translations(tr))
        return translations
