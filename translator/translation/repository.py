import json
import sqlite3
from typing import Union

from translator.translation.client import TranslationResult


class TranslationRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def add_word(self, source_word: str, data: str, session_id: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO 
                REQUESTED_WORDS(session_id, source_word, data)
                VALUES(?, ?, ?)
                """,
                (session_id,
                 source_word,
                 data
                 )
            )
        finally:
            cursor.close()

    def get_by_word(self, input_word) -> Union[TranslationResult, None]:
        if input_word is None or not input_word:
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """
                SELECT data
                FROM REQUESTED_WORDS
                WHERE source_word = :word
                """,
                {'word': input_word}
            )
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                return TranslationResult(json.loads(row[0]))
        finally:
            cursor.close()


