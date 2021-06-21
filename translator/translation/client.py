from typing import Dict, Any
from func import objectify
import json
import requests

from config import Config


class DictionaryLookupApi:
    """
    The class implements access to https://dictionaryapi.dev/ | https://github.com/meetDeveloper/freeDictionaryAPI
    """

    def __init__(self, config: Config):
        self.config = config

    def translate(self, inpt: str):
        resource = '/api/v2/entries/{language_code}/{word}'.format(language_code=self.config.language_code, word=inpt)
        url = self._get_url(self.config, resource)
        response = requests.request("GET", url)
        if response.status_code == requests.codes.ok:
            return TranslationResult(response.json())
        else:
            response.raise_for_status()

    def _get_url(self, config: Config, resources: str) -> str:
        return "https://{}{}".format(config.host, resources)


class TranslationResult:
    """A class for LookupResponse

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

    def __init__(self, data: Dict[str, Any]):
        """Assume only one element in source array exists"""
        if not self._is_source_dict_valid(data):
            raise Exception("Invalid dictionary for LookupResponse: {data}")
        self.output = objectify(data)[0]

    def is_empty(self) -> bool:
        return not self.output.__dict__.get('word')

    def to_dict(self) -> dict:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def _is_source_dict_valid(self, data: Dict[str, Any]) -> bool:
        return len(data) == 1 and \
               data[0] is not None
