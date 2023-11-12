from configparser import ConfigParser


class Config():
    DEFAULT_CONFIG_FILE_PATH = "config.ini"
    def __init__(self) -> None:
        self._g = self._init_config_parser()

    @property
    def g(self)  -> ConfigParser:
        return self._g

    def _init_config_parser(self) -> ConfigParser:
        config = ConfigParser()
        config.read(Config.DEFAULT_CONFIG_FILE_PATH)
        return config