from abc import ABC, abstractmethod


class Publisher(ABC):
    def __init__(self, host='localhost', username='', password='', port=1883):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self, to, data):
        pass

    @abstractmethod
    def disconnect(self):
        pass
