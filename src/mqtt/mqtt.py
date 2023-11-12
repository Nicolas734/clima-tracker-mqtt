import paho.mqtt.client as mqtt
from utils.config import Config
from utils.singleton import Singleton


class MqttClient(metaclass=Singleton):
    def __init__(self, config: Config=None) -> None:
        self._config = (config or Config())
        self._packets = []
        self._load_configs()
        self._mqtt_client = self._create_connection_and_set_callbacks()

    def _load_configs(self):
        self._broker = self._config.g.get("mqtt", "broker")
        self._topic = self._config.g.get("mqtt", "topic")
        self._port = self._config.g.getint("mqtt", "port")


    def on_connect(self, con, userdata, flags, rc):
        print("Start mqtt")
        con.subscribe(self._topic)


    def on_message(self,con, userdata, msg):
        payload = msg.payload.decode('utf-8')
        self._packets.append(payload)
        print(payload)


    def _create_connection_and_set_callbacks(self) -> mqtt.Client:
        conn = mqtt.Client(clean_session=True, reconnect_on_failure=True)
        conn.on_connect = self.on_connect
        conn.on_message = self.on_message
        return conn