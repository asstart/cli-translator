from client import DictionaryLookupApi, TranslationResult
from repository import TranslationRepository
from typing import Union
import json


class TranslateController:

    def __init__(self, api_client: DictionaryLookupApi,
                 repository: TranslationRepository):
        self.api_client = api_client
        self.repository = repository

    def translate(self, input_word: str, session_id: str) -> Union[TranslationResult, None]:
        card = self._get_from_db_if_exists(input_word)
        return card if card else self._get_from_api_if_exists(input_word, session_id)

    def _get_from_api_if_exists(self, input_word, session_id: str) -> Union[TranslationResult, None]:
        lookup_res = self.api_client.translate(input_word)
        if lookup_res.is_empty():
            return None
        else:
            self.repository.add_word(input_word, lookup_res.to_json(), session_id)
            return lookup_res

    def _get_from_db_if_exists(self, input_word: str) -> Union[TranslationResult, None]:
        translation = self.repository.get_by_word(input_word)
        return TranslationResult(json.loads(translation)) if translation else None
