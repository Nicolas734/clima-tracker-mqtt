import paho.mqtt.client as mqtt
from utils.config import Config
from utils.singleton import Singleton
from threading  import Lock, Thread
import time
from db.mongo import TemperatureCollection
from time import sleep
from json import dumps, loads


class MqttClient(metaclass=Singleton):
    def __init__(self, config: Config=None, db: TemperatureCollection = None) -> None:
        self._config = (config or Config())
        self._collection = (db or TemperatureCollection())
        self._packets = []
        self._load_configs()
        self._mqtt_client = self._create_connection_and_set_callbacks()
        self._thread = None
        self._iniciate_atributes()

    def _iniciate_atributes(self):
        self._keep_thread_running = True
        self.__lock = Lock()

    @property
    def thread_running(self) -> bool:
        """Return the running thread status."""
        self.__lock.acquire()
        ret = self._keep_thread_running
        self.__lock.release()
        return ret

    def _load_configs(self):
        self._broker = self._config.g.get("mqtt", "broker")
        self._topic = self._config.g.get("mqtt", "topic")
        self._port = self._config.g.getint("mqtt", "port")


    def on_connect(self, con, userdata, flags, rc):
        print("Start mqtt")
        con.subscribe(self._topic)


    def on_message(self,con, userdata, msg):
        payload = msg.payload.decode('utf-8')
        is_empty = self.verify_if_packet_is_empty(payload)
        if not is_empty:
            self._packets.append(payload)
        print(payload)


    def _create_connection_and_set_callbacks(self) -> mqtt.Client:
        conn = mqtt.Client()
        conn.on_connect = self.on_connect
        conn.on_message = self.on_message
        return conn

    def verify_if_packet_is_empty(self, packet: dict) -> bool:
        if packet == {}:
            return True
        else:
            return False

    def run(self):
        self._mqtt_client.connect(self._broker, self._port, 60)
        self._mqtt_client.loop_start()
        while True:
            if (int(time.time()) % 1600) == 0:
                for packet in self._packets:
                    self._collection.set_dict(loads(packet))
                    self._packets.pop()
                sleep(1)

    def run_and_check_threads(self):
        if self._thread is None:
            self._thread = Thread(target=self.run, name="temperature_collection")
            self._thread.start()
        else:
            if not self._thread.is_alive():
                self._thread = Thread(target=self.run, name="temperature_collection")
                self._thread.start()