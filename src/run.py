from utils.config import Config
from mqtt.mqtt import MqttClient

config = Config()
mqtt_client = MqttClient()
mqtt_client.run_and_check_threads()