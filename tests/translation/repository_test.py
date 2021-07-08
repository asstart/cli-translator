import json
from unittest.mock import MagicMock

from nose.tools import assert_equal, assert_is_none, assert_true, assert_in

from translator.translation.client import TranslationResult
from translator.translation.repository import TranslationRepository


class TestDataLoading(object):

    def test_empty_row(self):
        connection_mock = MagicMock()
        cursor_mock = MagicMock()
        connection_mock.cursor = cursor_mock
        cursor_mock.return_value.fetchone = MagicMock(return_value=None)

        repository = TranslationRepository(connection_mock)
        res = repository.get_by_word("car")

        assert_is_none(res)
        connection_mock.cursor.assert_called_once()
        cursor_mock.return_value.fetchone.assert_called_once()
        cursor_mock.return_value.close.assert_called_once()

        query_param = """
                SELECT data
                FROM REQUESTED_WORDS
                WHERE source_word = :word
                """
        map_param = {'word': "car"}

        cursor_mock.return_value.execute.assert_called_once_with(query_param, map_param)

    def test_single_row(self):
        connection_mock = MagicMock()
        cursor_mock = MagicMock()
        connection_mock.cursor = cursor_mock

        translation_data = json.dumps([{
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

        cursor_mock.return_value.fetchone = MagicMock(return_value=(translation_data,))

        repository = TranslationRepository(connection_mock)
        search_word = "car"

        result = repository.get_by_word(search_word)

        connection_mock.cursor.assert_called_once()
        cursor_mock.return_value.fetchone.assert_called_once()
        cursor_mock.return_value.close.assert_called_once()

        query_param = """
                SELECT data
                FROM REQUESTED_WORDS
                WHERE source_word = :word
                """
        map_param = {'word': f"{search_word}".format(search_word=search_word)}

        cursor_mock.return_value.execute.assert_called_once_with(query_param, map_param)

        assert_true(type(result) is TranslationResult)
        assert_equal(search_word, result.word)
        assert_equal(1, len(result.phonetics))
        assert_equal("/kɑr/", result.phonetics[0].text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", result.phonetics[0].audio)
        assert_equal(1, len(result.meanings))
        assert_equal("noun", result.meanings[0].partOfSpeech)
        assert_equal(1, len(result.meanings[0].definitions))
        assert_equal(
            "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people."
            , result.meanings[0].definitions[0].definition)
        assert_equal("she drove up in a car", result.meanings[0].definitions[0].example)
        assert_equal(3, len(result.meanings[0].definitions[0].synonyms))
        assert_in("automobile", result.meanings[0].definitions[0].synonyms)
        assert_in("motor", result.meanings[0].definitions[0].synonyms)
        assert_in("machine", result.meanings[0].definitions[0].synonyms)

    def test_none_word_return_none(self):
        connection_mock = MagicMock()

        repository = TranslationRepository(connection_mock)
        res = repository.get_by_word(None)

        assert_is_none(res)
        connection_mock.cursor.assert_not_called()

    def test_empty_word_return_none(self):
        connection_mock = MagicMock()

        repository = TranslationRepository(connection_mock)
        res = repository.get_by_word("")

        assert_is_none(res)
        connection_mock.cursor.assert_not_called()
