import socket
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Client.RequestsClass import Request
from Server.utils import *
from Server.ResponseClass import Response
from Client.ClientSockClass import ClientSocket

sock = ClientSocket(socket.gethostbyname(socket.gethostname()))
sock.connect()
request = Request(rq_type=METHOD_BUY, rq_data=[('A','C'), ('C', 'B')], client_token="ee250f4a9e41b93bb1e2627df36c796cee1678caf988d286a7181890e3ac7388")
rq_json = request.to_json()

msg_len = len(rq_json)
send_len = str(msg_len).encode(FORMAT)
send_len += b' ' * (MAX_PKT_SIZE - len(send_len))
sock.client_socket.send(send_len)
sock.client_socket.send(rq_json.encode(FORMAT))
msg_len =sock.client_socket.recv(MAX_PKT_SIZE).decode(FORMAT)
msg = sock.client_socket.recv(int(msg_len)).decode(FORMAT)

sock.end()


print(msg)
