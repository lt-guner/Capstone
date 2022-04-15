import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.3"
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def reconnect(self):
        try:
            client.close()
            return self.connect()
        except socket.error as e:
            print(e)
