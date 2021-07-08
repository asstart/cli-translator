from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.style import Style
from translator.model import Translation
from typing import List


def render_translations(translation: List[Translation], console: Console):
    tables = []
    for tr in translation:
        table = Table(show_header=False)
        table.add_column("Source Word", style="dark_cyan", no_wrap=True)
        table.add_column("Word Info", width=50)
        table.add_row(tr.word, tr.meaning.part_of_speech, style="dark_cyan")

        if len(tr.phonetics) > 0:
            table.add_row("", tr.phonetics[0].text, style=Style(color="bright_cyan", bold=True))

        table.add_row("", "")

        if tr.meaning:
            table.add_row("", tr.meaning.part_of_speech, style=Style(color="bright_blue", bold=True))
            table.add_row("", "")
            if tr.meaning.definitions:
                for d in tr.meaning.definitions:
                    table.add_row("", d.definition, style=Style(color="spring_green1", bold=True))
                    table.add_row("", "")
                    table.add_row("", d.example, style=Style(color="blue_violet", bold=True))
                    table.add_row("", "")

                    if d.synonyms:
                        top_syns = d.synonyms if len(d.synonyms) < 5 else d.synonyms[0: 4]
                        for s in top_syns:
                            table.add_row("", s, style=Style(color="steel_blue3", bold=True))
                        table.add_row("", "")
        tables.append(table)

    for t in tables:
        console.print(t)


def render_word_not_found(word: str, console: Console):
    console.print(Text(f"No translations of word: \"{word}\" have found"))