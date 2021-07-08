import sqlite3
import uuid


class InitRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def init_translations_db(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                REQUESTED_WORDS
                (
                session_id VARCHAR(36),
                insert_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                source_word VARCHAR(100),
                data VARCHAR(4000)
                )
                """
            )
        finally:
            cursor.close()
