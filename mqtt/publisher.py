import paho.mqtt.client as paho
from paho import mqtt


class Publisher:
    def __init__(self, host='localhost', username='', password='', port=1883):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = paho.Client(
            client_id="stock-news-pub",
            userdata=None,
            protocol=paho.MQTTv5,
            reconnect_on_failure=True)

    def connect(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.connect(self.host, self.port)

    def publish(self, topic, message):
        self.client.publish(topic, message, qos=1)

    def disconnect(self):
        self.client.disconnect()
