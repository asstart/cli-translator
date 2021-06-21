from datetime import datetime
from typing import List, Union


class CsvWriter:

    def make_file(self, cards: List[dict]):
        with open(self._get_file_name(), "w") as f:
            f.writelines([self._format_card(card) for card in cards])

    def _get_file_name(self) -> str:
        return "{name}.csv".format(name=datetime.today().strftime("%Y_%d_%m__%H_%M"))

    def _format_card(self, card: dict) -> str:
        source_word = self._get_source_word(card)
        phonetics = self._get_phonetics(card)

        return "{source_word};{phonetics};y\n".format(
            source_word=source_word,
            phonetics=phonetics
        )

    def _get_source_word(self, card: dict) -> str:
        if not card["word"]:
            raise Exception("Empty word in {card}".format(card=card))
        return card["word"]

    def _get_phonetics(self, card: dict) -> Union[str, None]:
        template = "|{transcription}:{link_to_audio}|"
        result = []
        if card["phonetics"]:
            for phonetic in card["phonetics"]:
                result.append(
                    template.format(
                        transcription=phonetic.get("text"),
                        link_to_audio=phonetic.get("audio"))
                )
            return ", ".join(result)
        return None

    # def _get_meanings(self, card: dict) -> str:
    #     template = "|{part_of_speech}:{definitions}|"
    #     def_template = "|{definition}:{example}:{synonym}|"
    #     result = []
    #     if card["meanings"]:
    #         for meaning in card["meanings"]:
    #             meanings = []
    #             if meaning["definitions"]:
    #                 for defin in meaning["definitions"]:
    #                     definitons.append(
    #                         def_template.format(
    #                             definiton=defin.get("definition"),
    #                             example=defin.get("example"),
    #                             synonym=", ".join(defin.get("synonyms"))
    #                         )
    #                     )
    #             str_definitions = ", ".join(definitons)
    #             meaning_str = template.format(
    #                 part_of_speech=meaning.get("partOfSpeech"),
    #                 definitons=str_definitions
    #             )
    #             meanings.append(meaning_str)
    #

