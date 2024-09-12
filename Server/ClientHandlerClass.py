import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from hashlib import sha256

from Server.ResponseClass import Response
from Server.utils import *
from Client.RequestsClass import Request
import socket

class ClientHandler:

    def __init__(self, conn, addr):  
        self.conn = conn
        self.addr = addr
        self.client_username = None
        self.client_token = None
    
    def __update_token(self):
        self.client_token = sha256(self.client_username.encode(FORMAT)).hexdigest()
        
    def get_username(self, value):
        return self.client_username
    
    def set_username(self, username):
        if username:
            self.client_username = username
            self.__update_token()
        
    def get_token(self):
        return self.client_token
    
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

    def send_pkt(self, pkt: Response):
        status = False
        try:
            pkt_len = str(len(pkt.to_json())).encode(FORMAT)
            pkt_len += b' ' * (MAX_PKT_SIZE - len(pkt_len))
            self.conn.send(pkt_len)
            self.conn.send(pkt.to_json().encode(FORMAT))
            status = True
        except socket.error as err:
            print(f"Package transfer failed! {str(err)}\n")
        return status