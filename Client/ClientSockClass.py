import socket

class ClientSocket:
    __CONNECT_MSG = '!OK'
    __ENCOD_FORMAT = 'utf-8'

    def __init__(self, ip=''):
        self.addr = None
        self.ip = ip
        self.port = 8000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token = ''

    def connect(self):
        self.addr = (self.ip, self.port)
        try:
            self.client_socket.connect(self.addr)
            return 1
        except socket.error as e:
            return 0

    def end(self):
        self.client_socket.close()




