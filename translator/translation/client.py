from typing import Dict, Any, List
from translator.func import objectify
import json
import requests

from translator.config import Config


class DictionaryLookupApi:
    """
    The class implements access to https://dictionaryapi.dev/ | https://github.com/meetDeveloper/freeDictionaryAPI
    """

    def __init__(self, config: Config):
        if DictionaryLookupApi._is_conf_valid(config):
            self.config = config
        else:
            raise Exception(f"Configuration is invalid: {config}".format(config=config))

    @staticmethod
    def _is_conf_valid(config: Config) -> bool:
        return config is not None and \
               config.host is not None \
               and config.language_code is not None

    def translate(self, inpt: str):
        url = '{host}/api/v2/entries/{language_code}/{word}'.format(
            host=self.config.host, language_code=self.config.language_code, word=inpt)
        response = requests.request("GET", url)
        if response.ok:
            result_json = response.json()
            return TranslationResult(result_json) if self._is_translation_found(result_json) else None
        elif response.status_code == requests.codes.not_found:
            return None
        else:
            response.raise_for_status()

    @staticmethod
    def _is_translation_found(result) -> bool:
        return type(result) is list and len(result) > 0 and result[0]['word']


class TREncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        return o.__dict__


class TranslationResult:
    """A class for LookupResponse

    Only the first variant will be handled if several will return.

    Table below provides typical attributes of LookupResponse.
    Since attributes are dynamically provided there is not a guarantee
    that all of them will always be present.

    ==================              ==============================
    Attribute                       Description
    ==================              ==============================
    output                          word, phonetics, meanings
        word                        str
        phonetics                   List[phonetic]
            phonetic                text, audio
                text                str
                audio               str
        meanings                    List[meaning]
            meaning                 partOfSpeech, definitions
                partOfSpeech        str
                definitions         List[definition]
                    definition      definition, example, synonyms
                        definition  str
                        example     str
                        synonyms    List[synonym]
                            synonym str

    """

    def __init__(self, data: List[dict]):
        objectified = objectify(data[0])
        self.word = objectified.word
        self.phonetics = objectified.phonetics
        self.meanings = objectified.meanings

    def is_empty(self) -> bool:
        return not self.word

    def to_dict(self) -> dict:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps([self], cls=TREncoder)
