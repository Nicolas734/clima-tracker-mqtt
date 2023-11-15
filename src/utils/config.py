from configparser import ConfigParser
from os import getcwd


class Config():
    path = getcwd()
    DEFAULT_CONFIG_FILE_PATH = path+"/config.ini"

    def __init__(self) -> None:
        self._g = self._init_config_parser()

    @property
    def g(self)  -> ConfigParser:
        return self._g

    def _init_config_parser(self) -> ConfigParser:
        config = ConfigParser()
        config.read(Config.DEFAULT_CONFIG_FILE_PATH)
        return config