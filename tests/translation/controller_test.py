from unittest.mock import MagicMock
from translator.translation.translation_controller import TranslateController, Translation, Phonetic, Meaning, Definition
from translator.translation.client import TranslationResult
from nose.tools import assert_is_none, assert_true, assert_equal
from typing import List



class TestTranslation(object):

    def test_translate_empty_word(self):
        api_client = MagicMock()
        repository = MagicMock()

        session_id = "1"
        input_word = ""
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)
        assert_is_none(res)

        repository.get_by_word.assert_not_called()
        api_client.translate.assert_not_called()

    def test_translate_none_word(self):
        api_client = MagicMock()
        repository = MagicMock()

        session_id = "1"
        input_word = None
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)
        assert_is_none(res)

        repository.get_by_word.assert_not_called()
        api_client.translate.assert_not_called()

    def test_translate_word_with_single_meaning_existed_in_db(self):
        api_client = MagicMock()
        repository = MagicMock()

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
        repository.get_by_word.return_value = TranslationResult(content)

        session_id = "1"
        input_word = "car"
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)

        repository.get_by_word.assert_called_once_with(input_word)
        api_client.translate.assert_not_called()

        assert_true(type(res) is list)
        assert_equal(1, len(res))

        translation = res[0]
        assert_true(type(translation) is Translation)
        assert_equal(input_word, translation.word)
        assert_equal(1, len(translation.phonetics))

        phonetic = translation.phonetics[0]
        assert_true(type(phonetic) is Phonetic)
        assert_equal("/kɑr/", phonetic.text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", phonetic.audio_link)

        meaning = translation.meaning
        assert_true(type(meaning) is Meaning)
        assert_equal("noun", meaning.part_of_speech)
        assert_equal(1, len(meaning.definitions))

        definition = meaning.definitions[0]
        assert_true(type(definition) is Definition)
        assert_equal("A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
                     definition.definition)
        assert_equal("she drove up in a car", definition.example)
        assert_equal(3, len(definition.synonyms))

    def test_translate_word_with_several_meanings_existed_in_db(self):
        api_client = MagicMock()
        repository = MagicMock()

        content = [{
            "word": "phone",
            "phonetics": [{
                "text": "/foʊn/",
                "audio": "https://lex-audio.useremarkable.com/mp3/_phone_1_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "verb",
                "definitions": [{
                    "definition": "Call someone on the phone.",
                    "synonyms": ["telephone", "call", "call up", "give someone a call", "give someone a ring", "ring", "get someone on the phone", "get on the phone to", "get", "reach", "dial", "make a call", "place a call", "make a call to", "place a call to"],
                    "example": "he phoned her at work"
                }]
            }, {
                "partOfSpeech": "noun",
                "definitions": [{
                    "definition": "A telephone.",
                    "synonyms": ["telephone", "mobile phone", "mobile", "cell phone", "car phone", "radiotelephone", "cordless phone", "videophone", "extension"],
                    "example": "a few seconds later the phone rang"
                }, {
                    "definition": "Headphones or earphones."
                }]
            }]
        }]
        repository.get_by_word.return_value = TranslationResult(content)

        session_id = "1"
        input_word = "phone"
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)

        repository.get_by_word.assert_called_once_with(input_word)
        api_client.translate.assert_not_called()

        assert_true(type(res) is list)
        assert_equal(2, len(res))

        translation_1 = res[0]
        assert_true(type(translation_1) is Translation)
        assert_equal(input_word, translation_1.word)
        assert_equal(1, len(translation_1.phonetics))

        phonetic = translation_1.phonetics[0]
        assert_true(type(phonetic) is Phonetic)
        assert_equal("/foʊn/", phonetic.text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/_phone_1_us_1.mp3", phonetic.audio_link)

        meaning_1 = translation_1.meaning
        assert_true(type(meaning_1) is Meaning)
        assert_equal("verb", meaning_1.part_of_speech)
        assert_equal(1, len(meaning_1.definitions))

        definition_1 = meaning_1.definitions[0]
        assert_true(type(definition_1) is Definition)
        assert_equal("Call someone on the phone.",
                     definition_1.definition)
        assert_equal("he phoned her at work", definition_1.example)
        assert_equal(15, len(definition_1.synonyms))

        translation_2 = res[1]
        assert_true(type(translation_2) is Translation)
        assert_equal(input_word, translation_2.word)
        assert_equal(1, len(translation_2.phonetics))

        phonetic_2 = translation_2.phonetics[0]
        assert_true(type(phonetic_2) is Phonetic)
        assert_equal("/foʊn/", phonetic_2.text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/_phone_1_us_1.mp3", phonetic_2.audio_link)

        meaning_2 = translation_2.meaning
        assert_true(type(meaning_2) is Meaning)
        assert_equal("noun", meaning_2.part_of_speech)
        assert_equal(2, len(meaning_2.definitions))

        definition_2_1 = meaning_2.definitions[0]
        assert_true(type(definition_2_1) is Definition)
        assert_equal("A telephone.",
                     definition_2_1.definition)
        assert_equal("a few seconds later the phone rang", definition_2_1.example)
        assert_equal(9, len(definition_2_1.synonyms))

        definition_2_2 = meaning_2.definitions[1]
        assert_true(type(definition_2_2) is Definition)
        assert_equal("Headphones or earphones.",
                     definition_2_2.definition)
        assert_is_none(definition_2_2.example)
        assert_is_none(definition_2_2.synonyms)

    def test_translate_single_word_by_api(self):
        api_client = MagicMock()
        repository = MagicMock()

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
        api_client.translate.return_value = TranslationResult(content)
        repository.get_by_word.return_value = None

        session_id = "1"
        input_word = "car"
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)

        repository.get_by_word.assert_called_once_with(input_word)
        api_client.translate.assert_called_once_with(input_word)

        assert_true(type(res) is list)
        assert_equal(1, len(res))

        translation = res[0]
        assert_true(type(translation) is Translation)
        assert_equal(input_word, translation.word)
        assert_equal(1, len(translation.phonetics))

        phonetic = translation.phonetics[0]
        assert_true(type(phonetic) is Phonetic)
        assert_equal("/kɑr/", phonetic.text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", phonetic.audio_link)

        meaning = translation.meaning
        assert_true(type(meaning) is Meaning)
        assert_equal("noun", meaning.part_of_speech)
        assert_equal(1, len(meaning.definitions))

        definition = meaning.definitions[0]
        assert_true(type(definition) is Definition)
        assert_equal(
            "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
            definition.definition)
        assert_equal("she drove up in a car", definition.example)
        assert_equal(3, len(definition.synonyms))

    def test_translate_word_not_existed_in_dictionary(self):
        api_client = MagicMock()
        repository = MagicMock()

        api_client.translate.return_value = None
        repository.get_by_word.return_value = None

        session_id = "1"
        inpt = "dslkgjlsdg"

        controller = TranslateController(api_client, repository)

        res = controller.translate(inpt, session_id)

        assert_is_none(res)

    def test_translate_unnormalized_word(self):
        api_client = MagicMock()
        repository = MagicMock()

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
        api_client.translate.return_value = TranslationResult(content)
        repository.get_by_word.return_value = None

        session_id = "1"
        input_word = "CAR"
        normalized_inpt = "car"
        controller = TranslateController(api_client, repository)

        res = controller.translate(input_word, session_id)

        repository.get_by_word.assert_called_once_with(normalized_inpt)
        api_client.translate.assert_called_once_with(normalized_inpt)

        assert_true(type(res) is list)
        assert_equal(1, len(res))

        translation = res[0]
        assert_true(type(translation) is Translation)
        assert_equal(normalized_inpt, translation.word)
        assert_equal(1, len(translation.phonetics))

        phonetic = translation.phonetics[0]
        assert_true(type(phonetic) is Phonetic)
        assert_equal("/kɑr/", phonetic.text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", phonetic.audio_link)

        meaning = translation.meaning
        assert_true(type(meaning) is Meaning)
        assert_equal("noun", meaning.part_of_speech)
        assert_equal(1, len(meaning.definitions))

        definition = meaning.definitions[0]
        assert_true(type(definition) is Definition)
        assert_equal(
            "A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people.",
            definition.definition)
        assert_equal("she drove up in a car", definition.example)
        assert_equal(3, len(definition.synonyms))
