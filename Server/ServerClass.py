from ClientHandlerClass import ClientHandler
from utils import HOST
import socket

class Server:
    _instance = None
    backlog_clients = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        
        return cls._instance

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Encerra o socket caso o programa seja encerrado
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def init_socket(self, port):
        status = False
        addr_socket = (HOST, port)

        try:
            #Bind do socket
            self.server_socket.bind(addr_socket)
            self.server_socket.listen(5)
            print(f"[SERVER] Server started at address {addr_socket[0]} and port {port}\n")

            status = True
        except:
            print("[SERVER] Failed to initialize socket!")

        return status
    
    @classmethod
    def add_client(cls, client):
        cls.backlog_clients[client] = None

    @classmethod
    def remove_client(cls, client):
        cls.backlog_clients.pop(client)


       



