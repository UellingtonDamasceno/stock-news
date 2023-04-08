import paho.mqtt.client as paho
from clients.publisher import Publisher
from paho import mqtt


class MqttPublisher(Publisher):
    def __init__(self, host="localhost", username="", password="", port=1883):
        super().__init__(host, username, password, port)
        self.client = paho.Client(
            client_id="stock-news-pub",
            userdata=None,
            protocol=paho.MQTTv5,
            reconnect_on_failure=True)

    def connect(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.connect(self.host, self.port)

    def publish(self, topic, data):
        self.client.publish(topic, data, qos=1)

    def disconnect(self):
        self.client.disconnect()
