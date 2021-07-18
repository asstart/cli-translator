from datetime import datetime
from typing import List, Union

from translator.model import Translation, Meaning, Phonetic


class Card:

    def __init__(self, word: str, phonetic_audio: str,
                 transcription: str, part_of_speech: str,
                 definition: str, example: str, synonyms: str):
        self.word = word
        self.phonetic_audio = phonetic_audio
        self.transcription = transcription
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.example = example
        self.synonyms = synonyms


class CsvWriter:

    def make_file(self, translations: List[Translation]):
        with open(self._get_file_name(), "w") as f:
            f.writelines([self._format_card(translation) for translation in translations])

    def _get_file_name(self) -> str:
        return "{name}.csv".format(name=datetime.today().strftime("%Y_%d_%m__%H_%M"))

    def _format_card(self, translation: Translation) -> Union[str, None]:
        card = self._translation_to_card(translation)

        return None if card is None else "{source_word};{phonetics};{part_of_speech};{definition};{example};{syns};y\n".format(
            source_word=card.word,
            phonetics=card.transcription,
            part_of_speech=card.part_of_speech,
            definition=card.definition,
            example=card.example,
            syns=card.synonyms
        )

    def _translation_to_card(self, translation: Translation) -> Union[Card, None]:
        if translation is None or translation.word is None:
            return None

        audio_link = self._extract_top_audio_link(translation.phonetics)
        transcription = self._extract_top_transcription(translation.phonetics)
        part_of_speech = self._extract_part_of_speech(translation.meaning)
        definition = self._extract_top_definition(translation.meaning)
        example = self._extract_top_example(translation.meaning)
        synonyms = self._extract_top_synonyms(translation.meaning)

        return Card(translation.word, audio_link, transcription, part_of_speech, definition, example, synonyms)

    @staticmethod
    def _extract_top_audio_link(phonetics: List[Phonetic]) -> Union[str, None]:
        if phonetics is None or len(phonetics) == 0:
            return None
        return phonetics[0].audio_link

    @staticmethod
    def _extract_top_transcription(phonetics: List[Phonetic]) -> Union[str, None]:
        if phonetics is None or len(phonetics) == 0:
            return None
        return phonetics[0].text

    @staticmethod
    def _extract_part_of_speech(meaning: Meaning) -> Union[str, None]:
        if meaning is None:
            return None
        return meaning.part_of_speech.replace(";", ",")

    @staticmethod
    def _extract_top_definition(meaning: Meaning) -> Union[str, None]:
        if meaning is None or \
                meaning.definitions is None \
                or len(meaning.definitions) == 0 or \
                meaning.definitions[0].definition is None:
            return None
        return meaning.definitions[0].definition.replace(";", ",")

    @staticmethod
    def _extract_top_example(meaning: Meaning) -> Union[str, None]:
        if meaning is None or \
                meaning.definitions is None \
                or len(meaning.definitions) == 0 or \
                meaning.definitions[0].example is None:
            return None
        return meaning.definitions[0].example.replace(";", ",")

    @staticmethod
    def _extract_top_synonyms(meaning: Meaning) -> Union[str, None]:
        if meaning is None or \
                meaning.definitions is None \
                or len(meaning.definitions) == 0 or \
                meaning.definitions[0].synonyms is None or \
                not meaning.definitions[0].synonyms:
            return None
        synonyms = meaning.definitions[0].synonyms
        top_synonyms = synonyms if len(synonyms) < 5 else synonyms[0:4]
        return ", ".join(top_synonyms).replace(";", ",")
