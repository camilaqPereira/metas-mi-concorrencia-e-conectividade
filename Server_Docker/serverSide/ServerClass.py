from server.requests import ConstantsManagement
from serverSide.ClientHandlerClass import ClientHandler
import socket
from threading import Lock

class Server:
    _instance = None
    backlog_clients:list[ClientHandler] = []
    backlog_lock = Lock()

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
        addr_socket = (ConstantsManagement.HOST.value, port)

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
    def add_client(cls, client:ClientHandler):
        with cls.backlog_lock:
            cls.backlog_clients.append(client)

    @classmethod
    def remove_client(cls, client:ClientHandler):
        with cls.backlog_clients:
            cls.backlog_clients.remove(client)


       



