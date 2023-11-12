import paho.mqtt.client as mqtt
from utils.config import Config

config = Config()

broker = config.g.get("mqtt","broker") or None
topic = config.g.get("mqtt", "topic") or None
port = config.g.getint("mqtt", "port") or None


def on_connect(con, userdata, flags, rc):
    print("Start mqtt")
    con.subscribe(topic)

def on_message(con, userdata, msg):
    payload = msg.payload.decode('utf-8')
    print(payload)



con = mqtt.Client()
con.on_connect = on_connect
con.on_message = on_message

con.connect(broker, port, 60)

con.loop_forever()