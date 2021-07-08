import requests
from translator.translation.client import DictionaryLookupApi, TranslationResult
from translator.config import Config
from nose.tools import assert_is_not_none, raises, assert_equal, assert_true, assert_in, assert_is_none
from unittest.mock import Mock, patch
from requests.models import Response
import json


class TestUrlBuilding(object):

    @patch("translator.translation.client.requests.request")
    def test_404_response_should_return_none(self, mocked_request):
        host = "http://schema_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        mocked_request.return_value.ok = False
        mocked_request.return_value.status_code = 404
        mocked_request.return_value.raise_for_status.side_effect = Exception()

        res = client.translate("word")

        assert_is_none(res)


    @patch("translator.translation.client.requests.request")
    def test_with_schema_host(self, mocked_request):
        host = "http://schema_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        mocked_request.return_value.ok = True
        mocked_request.return_value.json.return_value = [{"word":"car"}]

        client.translate("word")

        mocked_request.assert_called_once_with("GET", "http://schema_host/api/v2/entries/en_US/word")


class TestTranslation(object):

    @patch("translator.translation.client.requests.request")
    @raises(Exception)
    def test_return_value_not_ok_should_raise_exception(self, mock_request):
        """If return code isn't ok exception should be raised"""
        host = "valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        mock_request.return_value.ok = False
        mock_request.return_value.raise_for_status.side_effect = Exception()

        inpt = "word"
        client.translate(inpt)

        mock_request.assert_called_once_with("GET", "https://valid_host/api/v2/entries/en_US/car")

    @patch("translator.translation.client.requests.request")
    def test_return_value_ok_should_return_expected(self, mock_request):
        """Word with 1 meaning should be parsed correct"""
        host = "https://valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        response_content = [{
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

        mock_request.return_value.ok = True
        mock_request.return_value.json.return_value = response_content

        inpt = "car"
        result = client.translate(inpt)

        assert_true(type(result) is TranslationResult)
        mock_request.assert_called_once_with("GET", "https://valid_host/api/v2/entries/en_US/car")
        mock_request.return_value.json.assert_called_once()
        assert_equal(inpt, result.word)
        assert_equal(1, len(result.phonetics))
        assert_equal("/kɑr/", result.phonetics[0].text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/car_us_1.mp3", result.phonetics[0].audio)
        assert_equal(1, len(result.meanings))
        assert_equal("noun", result.meanings[0].partOfSpeech)
        assert_equal(1, len(result.meanings[0].definitions))
        assert_equal("A four-wheeled road vehicle that is powered by an engine and is able to carry a small number of people."
                     , result.meanings[0].definitions[0].definition)
        assert_equal("she drove up in a car", result.meanings[0].definitions[0].example)
        assert_equal(3, len(result.meanings[0].definitions[0].synonyms))
        assert_in("automobile", result.meanings[0].definitions[0].synonyms)
        assert_in("motor", result.meanings[0].definitions[0].synonyms)
        assert_in("machine", result.meanings[0].definitions[0].synonyms)

    @patch("translator.translation.client.requests.request")
    def test_translate_word_with_several_meanings(self, mocked_request):
        """Word with several meanings should be parsed correct"""
        host = "https://valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        response_content = [{
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

        mocked_request.return_value.ok = True
        mocked_request.return_value.json.return_value = response_content

        inpt = "phone"
        result = client.translate(inpt)

        mocked_request.assert_called_once_with("GET", "https://valid_host/api/v2/entries/en_US/phone")
        assert_true(type(result) is TranslationResult)

        assert_equal(inpt, result.word)
        assert_equal(1, len(result.phonetics))
        assert_equal("/foʊn/", result.phonetics[0].text)
        assert_equal("https://lex-audio.useremarkable.com/mp3/_phone_1_us_1.mp3", result.phonetics[0].audio)
        assert_equal(2, len(result.meanings))
        verb_meaning = result.meanings[0]
        assert_equal("verb", verb_meaning.partOfSpeech)
        assert_equal(1, len(verb_meaning.definitions))
        assert_equal("Call someone on the phone.", verb_meaning.definitions[0].definition)
        assert_equal("he phoned her at work", verb_meaning.definitions[0].example)
        assert_equal(15, len(verb_meaning.definitions[0].synonyms))
        assert_in("telephone", verb_meaning.definitions[0].synonyms)
        assert_in("call", verb_meaning.definitions[0].synonyms)
        assert_in("call up", verb_meaning.definitions[0].synonyms)
        assert_in("give someone a call", verb_meaning.definitions[0].synonyms)
        assert_in("give someone a ring", verb_meaning.definitions[0].synonyms)
        assert_in("ring", verb_meaning.definitions[0].synonyms)
        assert_in("get someone on the phone", verb_meaning.definitions[0].synonyms)
        assert_in("get on the phone to", verb_meaning.definitions[0].synonyms)
        assert_in("get", verb_meaning.definitions[0].synonyms)
        assert_in("reach", verb_meaning.definitions[0].synonyms)
        assert_in("dial", verb_meaning.definitions[0].synonyms)
        assert_in("make a call", verb_meaning.definitions[0].synonyms)
        assert_in("place a call", verb_meaning.definitions[0].synonyms)
        assert_in("make a call to", verb_meaning.definitions[0].synonyms)
        assert_in("place a call to", verb_meaning.definitions[0].synonyms)
        noun_meaning = result.meanings[1]
        assert_equal("noun", noun_meaning.partOfSpeech)
        assert_equal(2, len(noun_meaning.definitions))
        assert_equal("A telephone.", noun_meaning.definitions[0].definition)
        assert_equal("a few seconds later the phone rang", noun_meaning.definitions[0].example)
        assert_equal(9, len(noun_meaning.definitions[0].synonyms))
        assert_in("telephone", noun_meaning.definitions[0].synonyms)
        assert_in("mobile phone", noun_meaning.definitions[0].synonyms)
        assert_in("mobile", noun_meaning.definitions[0].synonyms)
        assert_in("cell phone", noun_meaning.definitions[0].synonyms)
        assert_in("car phone", noun_meaning.definitions[0].synonyms)
        assert_in("radiotelephone", noun_meaning.definitions[0].synonyms)
        assert_in("cordless phone", noun_meaning.definitions[0].synonyms)
        assert_in("videophone", noun_meaning.definitions[0].synonyms)
        assert_in("extension", noun_meaning.definitions[0].synonyms)
        assert_equal("Headphones or earphones.", noun_meaning.definitions[1].definition)
        assert_is_none(noun_meaning.definitions[1].example)
        assert_is_none(noun_meaning.definitions[1].synonyms)

    @patch("translator.translation.client.requests.request")
    def test_translate_with_several_translation_results(self, mocked_request):
        host = "https://valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        response_content = [{
            "word": "cat",
            "phonetics": [{
                "text": "/kæt/",
                "audio": "https://lex-audio.useremarkable.com/mp3/cat_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "noun"
            }]
        },{
            "word": "CAT",
            "phonetics": [{
                "text": "/kæt/",
                "audio": "https://lex-audio.useremarkable.com/mp3/cat_us_1.mp3"
            }],
            "meanings": [{
                "partOfSpeech": "abbreviation",
                "definitions": [{
                    "definition": "short for \"computerized axial tomography\""
                }, {
                    "definition": "Computer-assisted (or -aided) testing."
                }, {
                    "definition": "Clear air turbulence."
                }]
            }]
        }]

        mocked_request.return_value.ok = True
        mocked_request.return_value.json.return_value = response_content

        inpt = "cat"
        result = client.translate(inpt)

        assert_equal(inpt, result.word)
        assert_equal("noun", result.meanings[0].partOfSpeech)

    @patch("translator.translation.client.requests.request")
    def test_word_not_found(self, mocked_request):
        host = "https://valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)

        response_content = {
            "title": "No Definitions Found",
            "message": "Sorry pal, we couldn't find definitions for the word you were looking for.",
            "resolution": "You can try the search again at later time or head to the web instead."
        }

        mocked_request.return_value.ok = True
        mocked_request.return_value.json.return_value = response_content

        inpt = "dslkgjlsdkg"

        res = client.translate(inpt)

        assert_is_none(res)


class TestClientInitialization(object):

    @raises(Exception)
    def test_no_hostname_should_raise_exception(self):
        """If hostname in config is empty exception should be thrown"""
        host = None
        lang_source = "en"
        conf = Config(host, lang_source)
        DictionaryLookupApi(conf)

    @raises(Exception)
    def test_no_langsource_should_raise_exception(self):
        """If lang_source in config is empty exception should be thrown"""
        host = "http://some_host"
        lang_source = None
        conf = Config(host, lang_source)
        DictionaryLookupApi(conf)

    @raises(Exception)
    def test_none_config_should_raise_exception(self):
        """If config is None exception should be thrown"""
        DictionaryLookupApi(None)

    def test_valid_conf(self):
        """DictionaryLookupApi instantiation should be expected
        with valid Config"""
        host = "http://valid_host"
        lang_source = "en_US"
        conf = Config(host, lang_source)
        client = DictionaryLookupApi(conf)
        assert_is_not_none(client)
        assert_equal(conf, client.config)
