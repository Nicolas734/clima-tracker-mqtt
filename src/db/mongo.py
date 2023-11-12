from utils.config import Config
from pymongo.mongo_client import MongoClient
from threading  import Lock
from utils.singleton import Singleton
from utils.config import Config

class Mongo(metaclass=Singleton):
    def __init__(self, config: Config = None):
        self._config = (config or Config())
        self._load_configs()
        self._conn = self._create_mongo_db_client()
        self.__lock = Lock()

    def _load_configs(self):
        self._uri = self._config.g.get("mongo", "uri")
        self._database = self._config.g.get("mongo", "database")


    def _create_mongo_db_client(self):
        client = MongoClient(self._uri)
        conn =client.get_database(name="ClimaTracker")
        return conn


    def select(self, col: str) -> list:
        self.__lock.acquire()
        collection = self._conn.get_collection(name=col)
        dicts = collection.find()
        self.__lock.release()
        return dicts


    def insert(self, col: str, dict: dict):
        self.__lock.acquire()
        collection = self._conn.get_collection(name=col)
        new_dict = collection.insert_one(dict)
        self.__lock.release()
        return new_dict



class TemperatureCollection():
    def __init__(self) -> None:
        self._db = Mongo()
        self._collection = "temperature"

    @property
    def db(self) -> Mongo:
        return self._db

    def get_all_dicts(self):
        dicts = self._db.select(self._collection)
        return dicts

    def set_dict(self, dict: dict):
        res = self._db.insert(col = self._collection, dict = dict)
        return res
