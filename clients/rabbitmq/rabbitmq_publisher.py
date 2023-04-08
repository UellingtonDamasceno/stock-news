import pika as client
from clients.publisher import Publisher


class RabbitMQPublisher(Publisher):
    def __init__(self, host="localhost", username="", password="",  port=5672, routing_key=""):
        super().__init__(host, username, password, port)
        self.queue_name = routing_key
        self.connection = None
        self.channel = None

    def connect(self):
        parms = client.URLParameters(self.host)
        self.connection = client.BlockingConnection(parms)
        self.channel = self.connection.channel()

    def send(self, queue_name="", data=""):
        queue_name = self.queue_name if queue_name == "" else queue_name
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange='', routing_key=queue_name, body=data,
            properties=client.BasicProperties(delivery_mode=2)
        )

    def disconnect(self):
        self.channel.close()
        self.connection.close()
