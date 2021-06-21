from dataclasses import dataclass
from typing import Union

import yaml


@dataclass
class Config:
    host: str
    language_code: str


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
                return Config(cfg.get('host'), cfg.get("language_code"))
        except OSError as err:
            print("Something goes wrong during file opening: {}".format(err.strerror))
            return None

    def merge(self, file_conf: Union[Config, None]) -> Config:
        """
        Configs from appilication.yml will merge with default values
        """
        if file_conf:
            merged_conf = Config(
                file_conf.host if file_conf.host else "api.dictionaryapi.dev",
                file_conf.language_code if file_conf.language_code else "en_US"
            )
        else:
            merged_conf = Config(
                "api.dictionaryapi.dev",
                "en_US"
            )
        if self.is_config_valid(merged_conf):
            return merged_conf
        else:
            raise Exception("Invalid config: {}".format(merged_conf))

    @staticmethod
    def is_config_valid(cfg: Config) -> bool:
        return cfg.host is not None \
               and cfg.language_code is not None
