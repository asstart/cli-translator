from typing import Dict, Any, List, Union
from translator.translation.client import TranslationResult


class Phonetic:

    def __init__(self, text: str, audio_link: str):
        self.text = text
        self.audio_link = audio_link


class Definition:

    def __init__(self, example: str, definition: str, synonyms: List[str]):
        self.example = example
        self.definition = definition
        self.synonyms = synonyms


class Meaning:

    def __init__(self, part_of_speech: str, definition: List[Definition]):
        self.part_of_speech = part_of_speech
        self.definitions = definition


class Translation:

    def __init__(self, word: str, phonetics: List[Phonetic], meaning: Meaning):
        self.word = word
        self.phonetics = phonetics
        self.meaning = meaning


def extract_meanings(translation_res: TranslationResult) -> List[Meaning]:
    meanings = []
    for meaning in translation_res.meanings:
        part_of_speech = meaning.partOfSpeech
        definitions = []
        for definition in meaning.definitions:
            definitions.append(Definition(definition.example, definition.definition, definition.synonyms))

        meanings.append(
            Meaning(part_of_speech, definitions)
        )
    return meanings


def extract_phonetics(translation_res: TranslationResult) -> List[Phonetic]:
    phonetics = []
    for phonetic in translation_res.phonetics:
        phonetics.append(Phonetic(phonetic.text, phonetic.audio))
    return phonetics


def tr_to_translations(translation_res: TranslationResult) -> List[Translation]:
    word = translation_res.word
    phonetics = extract_phonetics(translation_res)
    meanings = extract_meanings(translation_res)
    translations = []
    for meaning in meanings:
        translations.append(
            Translation(
                word,
                phonetics,
                meaning
            )
        )
    return translations
