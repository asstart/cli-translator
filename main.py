from __future__ import print_function, unicode_literals

import os
import sqlite3
import uuid

import click
from PyInquirer import style_from_dict, prompt, Token
from rich.console import Console

from translator.export.csvwriter import CsvWriter
from translator.config import ConfigReader
from translator.export.export_controller import ExportController
from translator.export.repository import ExportRepository
from translator.translation.translation_controller import TranslateController
from translator.translation.repository import TranslationRepository
from translator.render import render_translations, render_word_not_found
from translator.translation.client import DictionaryLookupApi
from translator.init.init_controller import InitController
from translator.init.repository import InitRepository


conf = ConfigReader().get_conf()

connection = sqlite3.Connection(conf.db_path)
connection.isolation_level = None
session_id = str(uuid.uuid4())
console = Console()

translate_controller = TranslateController(
    DictionaryLookupApi(conf),
    TranslationRepository(connection)
)

export_controller = ExportController(
    ExportRepository(connection),
    CsvWriter()
)

init_controller = InitController(InitRepository(connection))

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'input',
        'name': 'word',
        'message': 'Input word to translate'
    }
]


def translate_command():
    while True:
        do_translate()


def do_translate():
    init_controller.init_db()
    print("CLI Translator")
    answers = prompt(questions, style=style)
    os.system('clear')
    input_word = answers['word']
    if input_word == '-q':
        exit(0)
    elif input_word == '-e':
        export_controller.export_by_session(session_id)
        exit(0)
    else:
        translated = translate_controller.translate(input_word, session_id)
        if translated is not None:
            render_translations(translated, console)
        else:
            render_word_not_found(input_word, console)


def export_command():
    export_controller.export_all()


@click.group()
def cli():
    pass


@click.command()
def translate():
    """
    Use this to start translator
    :return:
    """
    translate_command()


@click.command()
def export():
    """
    Use this to export cards to csv file
    :return:
    """
    export_command()


cli.add_command(translate)
cli.add_command(export)

if __name__ == '__main__':
    cli()
