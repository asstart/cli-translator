# from __future__ import print_function, unicode_literals
#
# import os
# import sqlite3
# import uuid
#
# import click
# from PyInquirer import style_from_dict, prompt, Token
# from rich.console import Console
#
# from translator.export.csvwriter import CardWriter
# from config import ConfigReader
# from controller.export import ExportController
# from translation.translation_controller import TranslateController
# from repository.card_repository import CardRepository
# from render import render_anki_card, render_word_not_found
# from translation.client import DictionaryLookupApi
#
# db_path = "translator.db"
# conf_file_path = "application.yml"
#
# conf = ConfigReader(conf_file_path).get_conf()
# api_client = DictionaryLookupApi(conf)
# writer = CardWriter()
# connection = sqlite3.Connection(db_path)
# connection.isolation_level = None
# session_id = str(uuid.uuid4())
# repository = CardRepository(connection)
# console = Console()
#
# translate_controller = TranslateController(api_client, repository)
# export_controller = ExportController(repository, writer)
#
# style = style_from_dict({
#     Token.QuestionMark: '#E91E63 bold',
#     Token.Selected: '#673AB7 bold',
#     Token.Instruction: '',  # default
#     Token.Answer: '#2196f3 bold',
#     Token.Question: '',
# })
#
# questions = [
#     {
#         'type': 'input',
#         'name': 'word',
#         'message': 'Input word to translate'
#     }
# ]
#
#
# def translate_command():
#     while True:
#         do_translate()
#
#
# def do_translate():
#     print("CLI Translator")
#     answers = prompt(questions, style=style)
#     os.system('clear')
#     input_word = answers['word']
#     if input_word == '-q':
#         exit(0)
#     elif input_word == '-e':
#         export_controller.export_session(session_id)
#         exit(0)
#     else:
#         translated = translate_controller.translate(input_word, session_id)
#         if translated is not None:
#             render_anki_card(translated, console)
#         else:
#             render_word_not_found(input_word, console)
#
#
# def export_command():
#     export_controller.export_all()
#
#
# @click.group()
# def cli():
#     pass
#
#
# @click.command()
# def translate():
#     """
#     Use this to start translator
#     :return:
#     """
#     translate_command()
#
#
# @click.command()
# def export():
#     """
#     Use this to export cards to csv file
#     :return:
#     """
#     export_command()
#
#
# cli.add_command(translate)
# cli.add_command(export)
#
# if __name__ == '__main__':
#     cli()
