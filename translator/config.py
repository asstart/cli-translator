from dataclasses import dataclass
from typing import Union
from os.path import expanduser, join

import yaml


@dataclass
class Config:
    host: str = "https://api.dictionaryapi.dev"
    language_code: str = "en_US"
    db_path: str = join(expanduser("~"), ".cli_translator.db")


class ConfigReader:

    def __init__(self, file_path: str = 'application.yml'):
        self.file_path = file_path

    def get_conf(self) -> Config:
        return self.merge(
            self.try_read_conf_from_application_yml()
        )

    def try_read_conf_from_application_yml(self) -> Union[Config, None]:
        try:
            with open(self.file_path, "r") as file:
                cfg = yaml.load(file)
                return Config(cfg.get('host'), cfg.get("language_code"), cfg.get("db_path"))
        except OSError as err:
            print("Something goes wrong during file opening: {}".format(err.strerror))
            return None

    def merge(self, file_conf: Union[Config, None]) -> Config:
        return self.is_config_valid(file_conf) if file_conf else Config()

    @staticmethod
    def is_config_valid(cfg: Config) -> bool:
        return cfg.host is not None \
               and cfg.language_code is not None
