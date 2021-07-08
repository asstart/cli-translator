from .client import DictionaryLookupApi, TranslationResult
from .repository import TranslationRepository
from translator.model import tr_to_translations
from typing import Union
from translator.model import *


class TranslateController:

    def __init__(self, api_client: DictionaryLookupApi,
                 repository: TranslationRepository):
        self.api_client = api_client
        self.repository = repository

    def translate(self, input_word: str, session_id: str) -> Union[List[Translation], None]:
        if self._is_invalid(input_word):
            return None

        normalized_word = self._normalize_word(input_word)
        db_res = self._get_from_db_if_exists(normalized_word)
        tr_res = db_res if db_res else self._get_from_api_if_exists(normalized_word, session_id)
        if tr_res is None:
            return None
        else:
            return tr_to_translations(tr_res)

    def _get_from_api_if_exists(self, input_word, session_id: str) -> Union[TranslationResult, None]:
        translation_res = self.api_client.translate(input_word)
        if translation_res is None or translation_res.is_empty():
            return None
        else:
            self.repository.add_word(input_word, translation_res.to_json(), session_id)
            return translation_res

    def _get_from_db_if_exists(self, input_word: str) -> Union[TranslationResult, None]:
        translation_res = self.repository.get_by_word(input_word)
        return translation_res if translation_res else None

    def _normalize_word(self, word: str) -> str:
        return word.lower().strip()

    def _is_invalid(self, word: str) -> bool:
        return word is None or not word
