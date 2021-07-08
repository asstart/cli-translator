import json
from unittest.mock import MagicMock

from nose.tools import assert_equal, assert_true, assert_in

from translator.export.repository import ExportRepository
from translator.translation.client import TranslationResult


class TestRepository(object):

    def test_get_all_by_session(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        db_row = json.dumps([{
            "word": "car",
            "phonetics": [{
                "text": "/kɑr/",
                "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "noun",
                "definitions": [{
                    "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                    "synonyms": ["automobile", "motor", "machine"],
                    "example": "she drove up in a car"
                }]
            }]
        }])

        cursor.fetchall.return_value = [db_row]
        session_id = "1"

        repository = ExportRepository(connection)

        res = repository.get_all_by_session(session_id)

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                WHERE session_id = :id
                """
        map_param = {"id": session_id}

        cursor.execute.assert_called_once_with(query_param, map_param)

        assert_equal(1, len(res))
        translation = res[0]
        assert_true(type(translation) is TranslationResult)
        assert_equal("car", translation.word)
        assert_equal(1, len(translation.phonetics))
        assert_equal("/kɑr/", translation.phonetics[0].text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", translation.phonetics[0].audio)
        assert_equal(1, len(translation.meanings))
        assert_equal("noun", translation.meanings[0].partOfSpeech)
        assert_equal(1, len(translation.meanings[0].definitions))
        assert_equal(
            "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people."
            , translation.meanings[0].definitions[0].definition)
        assert_equal("she drove up in a car", translation.meanings[0].definitions[0].example)
        assert_equal(3, len(translation.meanings[0].definitions[0].synonyms))
        assert_in("automobile", translation.meanings[0].definitions[0].synonyms)
        assert_in("motor", translation.meanings[0].definitions[0].synonyms)
        assert_in("machine", translation.meanings[0].definitions[0].synonyms)

    def test_empty_get_all_by_session(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        cursor.fetchall.return_value = []
        session_id = "1"

        repository = ExportRepository(connection)

        res = repository.get_all_by_session(session_id)

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                WHERE session_id = :id
                """
        map_param = {"id": session_id}

        cursor.execute.assert_called_once_with(query_param, map_param)

        assert_equal(0, len(res))

    def test_get_by_session_several_rows(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        db_rows = [json.dumps([{
            "word": "car",
            "phonetics": [{
                "text": "/kɑr/",
                "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "noun",
                "definitions": [{
                    "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                    "synonyms": ["automobile", "motor", "machine"],
                    "example": "she drove up in a car"
                }]
            }]
        }]),
            json.dumps([{
                "word": "car",
                "phonetics": [{
                    "text": "/kɑr/",
                    "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
                }],
                "meanings": [{
                    "partOfSpeech": "noun",
                    "definitions": [{
                        "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                        "synonyms": ["automobile", "motor", "machine"],
                        "example": "she drove up in a car"
                    }]
                }]
            }])
        ]

        cursor.fetchall.return_value = db_rows
        session_id = "1"

        repository = ExportRepository(connection)

        res = repository.get_all_by_session(session_id)

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                WHERE session_id = :id
                """
        map_param = {"id": session_id}

        cursor.execute.assert_called_once_with(query_param, map_param)

        assert_equal(2, len(res))
        assert_true(type(res[0]) is TranslationResult)
        assert_true(type(res[1]) is TranslationResult)

    def test_get_all(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        db_row = json.dumps([{
            "word": "car",
            "phonetics": [{
                "text": "/kɑr/",
                "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "noun",
                "definitions": [{
                    "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                    "synonyms": ["automobile", "motor", "machine"],
                    "example": "she drove up in a car"
                }]
            }]
        }])

        cursor.fetchall.return_value = [db_row]

        repository = ExportRepository(connection)

        res = repository.get_all()

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                """

        cursor.execute.assert_called_once_with(query_param)

        assert_equal(1, len(res))
        translation = res[0]
        assert_true(type(translation) is TranslationResult)
        assert_equal("car", translation.word)
        assert_equal(1, len(translation.phonetics))
        assert_equal("/kɑr/", translation.phonetics[0].text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", translation.phonetics[0].audio)
        assert_equal(1, len(translation.meanings))
        assert_equal("noun", translation.meanings[0].partOfSpeech)
        assert_equal(1, len(translation.meanings[0].definitions))
        assert_equal(
            "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people."
            , translation.meanings[0].definitions[0].definition)
        assert_equal("she drove up in a car", translation.meanings[0].definitions[0].example)
        assert_equal(3, len(translation.meanings[0].definitions[0].synonyms))
        assert_in("automobile", translation.meanings[0].definitions[0].synonyms)
        assert_in("motor", translation.meanings[0].definitions[0].synonyms)
        assert_in("machine", translation.meanings[0].definitions[0].synonyms)

    def test_empty_get_all(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        cursor.fetchall.return_value = []

        repository = ExportRepository(connection)

        res = repository.get_all()

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                """

        cursor.execute.assert_called_once_with(query_param)

        assert_equal(0, len(res))

    def test_get_all_several_rows(self):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor

        db_rows = [json.dumps([{
            "word": "car",
            "phonetics": [{
                "text": "/kɑr/",
                "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "noun",
                "definitions": [{
                    "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                    "synonyms": ["automobile", "motor", "machine"],
                    "example": "she drove up in a car"
                }]
            }]
        }]),
            json.dumps([{
                "word": "car",
                "phonetics": [{
                    "text": "/kɑr/",
                    "audio": "https://lex-audio.useremarkable.com/mp3/car_us_1.mp3"
                }],
                "meanings": [{
                    "partOfSpeech": "noun",
                    "definitions": [{
                        "definition": "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                        "synonyms": ["automobile", "motor", "machine"],
                        "example": "she drove up in a car"
                    }]
                }]
            }])
        ]

        cursor.fetchall.return_value = db_rows

        repository = ExportRepository(connection)

        res = repository.get_all()

        query_param = """
                SELECT data
                FROM TRANSLATIONS
                """

        cursor.execute.assert_called_once_with(query_param)

        assert_equal(2, len(res))
        assert_true(type(res[0]) is TranslationResult)
        assert_true(type(res[1]) is TranslationResult)
