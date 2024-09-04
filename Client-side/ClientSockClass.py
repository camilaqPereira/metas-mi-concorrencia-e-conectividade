import socket



class ClientSocket():
    def __init__(self):
        self.ip = ""
        self.port = 8000
        self.addr = (self.ip, self.port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip):
        self.ip = ip
        self.addr = (self.ip, self.port)
        self.client_socket.connect(self.addr)

    def end(self):
        self.client_socket.close()




