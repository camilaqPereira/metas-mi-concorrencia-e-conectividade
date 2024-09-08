import socket

class ClientSocket:
    __CONNECT_MSG = '!OK'
    __ENCOD_FORMAT = 'utf-8'

    def __init__(self):
        self.addr = None
        self.ip = ""
        self.port = 8000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = ''

    def connect(self, ip):
        self.ip = ip
        self.addr = (self.ip, self.port)
        try:
            self.client_socket.connect(self.addr)
            self.client_socket.recv(3)
            self.client_socket.send(self.__CONNECT_MSG.encode(self.__ENCOD_FORMAT))
            return 1
        except socket.error as e:
            return 0

    def end(self):
        self.client_socket.close()




