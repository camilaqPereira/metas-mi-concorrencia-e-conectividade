import socket
import time


def creat_new_conn():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(addr)

    return client_socket

def end_conn(client_socket:socket.socket):
    client_socket.close()

def send_request(client:socket.socket, msg:str):
    client.send(msg.encode('utf-8'))
    return True

IP = '172.16.103.10'
HEADER = 64
PORT = 8000
ADDR = (IP,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECTED"



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

msg = input('digite sua mensagem: ')
msg_len = len(msg)
send_len = str(msg_len).encode(FORMAT)
send_len += b' ' * (HEADER - len(send_len))
client_socket.send(send_len)
client_socket.send(msg.encode('utf-8'))

sleep(5)
client_socket.close()


