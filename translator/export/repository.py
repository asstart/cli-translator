import sqlite3
from typing import Union, List

class ExportRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def get_all_by_session(self, session_id: str) -> Union[List[str], None]:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT data
                FROM TRANSLATIONS
                WHERE session_id = :id
                """,
                {'id': session_id}
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all(self) -> Union[List[str], None]:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT data
                FROM TRANSLATIONS
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
