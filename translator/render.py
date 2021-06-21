from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.style import Style

from card import Card


def render_anki_card(card: Card, console: Console):
    table = Table(show_header=False)
    table.add_column("Source Word", style="dark_cyan", no_wrap=True)
    table.add_column("Word Info", width=50)

    table.add_row(card.source_word, card.part_of_speech, style="dark_cyan")

    if len(card.translations) > 0:
        table.add_row("", "")
        table.add_row("", "Translations", style=Style(color="bright_cyan", bold=True))
        for i in range(0, len(card.translations)):
            table.add_row("", card.translations[i], style="cyan2")

    if len(card.synonyms) > 0:
        table.add_row("", "")
        table.add_row("", "Synonyms", style=Style(color="bright_blue", bold=True))
        for i in range(0, len(card.synonyms)):
            table.add_row("", card.synonyms[i], style="sky_blue3")

    if len(card.examples) > 0:
        table.add_row("", "")
        table.add_row("", "Usage", style=Style(color="bright_green", bold=True))
        for i in range(0, len(card.examples)):
            table.add_row("", card.examples[i], style="dark_sea_green4")

    console.print(table)


def render_word_not_found(word: str, console: Console):
    console.print(Text(f"No translations of word: \"{word}\" have found"))