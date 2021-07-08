import json
import sqlite3
from typing import Union, List
from translator.translation.client import TranslationResult


class ExportRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def get_all_by_session(self, session_id: str) -> Union[List[TranslationResult], None]:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT data
                FROM REQUESTED_WORDS
                WHERE session_id = :id
                """,
                {'id': session_id}
            )
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append(TranslationResult(json.loads(row[0])))
            return result
        finally:
            cursor.close()

    def get_all(self) -> Union[List[TranslationResult], None]:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT data
                FROM REQUESTED_WORDS
                """
            )
            rows = cursor.fetchall()
            result = []
            for row in rows:
                result.append(TranslationResult(json.loads(row[0])))
            return result
        finally:
            cursor.close()
