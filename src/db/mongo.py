from utils.config import Config
import pymongo


class Mongo():
    def __init__(self, config: Config = None):
        self._config = (config or Config())
        self._load_configs()
        self._client = self._create_mongo_db_client()

    def _load_configs(self):
        self._uri = self._config.g.get("mongo", "uri")
        self._database = self._config.g.get("mongo", "database")

    def _create_mongo_db_client(self):
        client = pymongo.MongoClient(self._uri)
        return client.ClimaTracker