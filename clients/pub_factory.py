from clients.rabbitmq.rabbitmq_publisher import RabbitMQPublisher
from clients.mqtt.mqtt_publisher import MqttPublisher
from dotenv import load_dotenv
import os


class PublisherFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PublisherFactory, cls).__new__(cls)
            load_dotenv()
        return cls._instance

    def mqtt(self):
        host = str(os.getenv("MQTT_HOST"))
        port = int(os.getenv("MQTT_PORT"))
        username = str(os.getenv("MQTT_USERNAME"))
        password = str(os.getenv("MQTT_PASSWORD"))
        return self.mqtt(host, port, username, password)

    def rabbitmq(self):
        host = str(os.getenv("RABBITMQ_HOST"))
        port = int(os.getenv("RABBITMQ_PORT"))
        username = str(os.getenv("RABBITMQ_USERNAME"))
        password = str(os.getenv("RABBITMQ_PASSWORD"))
        routing_key = str(os.getenv("RABBITMQ_ROUTING_KEY"))
        return RabbitMQPublisher(host, username, password, port, routing_key)
