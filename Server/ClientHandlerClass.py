from hashlib import sha256
from Server.utils import *
from Client.RequestsClass import Request
import socket

class ClientHandler:

    def __init__(self, conn, addr):  
        self.conn = conn
        self.addr = addr
        self.client_username = ""
        self.client_token = None
        
    def receive_pkt(self):
        pkt = Request()

        try:
            pkt_size = self.conn.recv(MAX_PKT_SIZE).decode(FORMAT)
            if pkt_size:
                pkt_size = int(pkt_size)
                #recebendo segundo pacote -> mensagem
                pkt.from_json(self.conn.recv(pkt_size).decode(FORMAT))
                print(f"[SERVER]: Message received {self.addr} -> {pkt.to_json()}")
        except socket.error as err:
            print(f"[SERVER] Package reception failed! {str(err)}\n")

        return pkt

    def send_pkt(self, pkt):
        status = False
        try:
            pkt_len = str(len(pkt)).encode(FORMAT)
            pkt_len += b' ' * (MAX_PKT_SIZE - len(pkt_len))
            self.conn.send(pkt_len)
            self.conn.send(pkt.encode(FORMAT))
            status = True
        except socket.error as err:
            print(f"Package transfer failed! {str(err)}\n")
        return status