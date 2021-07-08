import json
from unittest.mock import MagicMock
from translator.export.export_controller import ExportController
from nose.tools import raises
from translator.translation.client import TranslationResult
from translator.model import *


class TestExport(object):

    @raises(Exception)
    def test_empty_session_throws(self):
        repository = MagicMock()
        writer = MagicMock()

        invalid_session = ""

        controller = ExportController(repository, writer)

        controller.export_by_session(invalid_session)

        repository.get_all_by_session.assert_not_called()
        writer.make_file.assert_not_called()

    @raises(Exception)
    def test_none_session_throws(self):
        repository = MagicMock()
        writer = MagicMock()

        invalid_session = None

        controller = ExportController(repository, writer)

        controller.export_by_session(invalid_session)

        repository.get_all_by_session.assert_not_called()
        writer.make_file.assert_not_called()


    def test_empty_by_session(self):
        repository = MagicMock()
        writer = MagicMock()

        session = "1"

        controller = ExportController(repository, writer)

        repository.get_all_by_session.return_value = []

        controller.export_by_session(session)

        repository.get_all_by_session.assert_called_once_with(session)
        writer.make_file.assert_not_called()

    def test_by_session(self):
        repository = MagicMock()
        writer = MagicMock()

        session = "1"

        controller = ExportController(repository, writer)

        content = [{
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
        }]

        repository.get_all_by_session.return_value = [TranslationResult(content)]

        controller.export_by_session(session)

        repository.get_all_by_session.assert_called_once_with(session)
        writer.make_file.assert_called_once()

    def test_empty_all(self):
        repository = MagicMock()
        writer = MagicMock()

        controller = ExportController(repository, writer)

        repository.get_all.return_value = []

        controller.export_all()

        repository.get_all.assert_called_once_with()
        writer.make_file.assert_not_called()

    def test_get_all(self):
        repository = MagicMock()
        writer = MagicMock()

        controller = ExportController(repository, writer)

        content = [{
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
        }]

        repository.get_all.return_value = [TranslationResult(content)]

        controller.export_all()

        repository.get_all.assert_called_once_with()
        writer.make_file.assert_called_once()