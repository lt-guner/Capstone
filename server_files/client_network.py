import socket
from time import sleep


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.15"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.addr)
            print('Connected to server')
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            self.reconnect()

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            self.reconnect()

    def reconnect(self):
        print('Connection lost... reconnecting')
        self.connected = False
        try:
            client.connect(self.addr)
            connected = True
            print('Reconnection successful')
        except socket.error:
            sleep(2)
