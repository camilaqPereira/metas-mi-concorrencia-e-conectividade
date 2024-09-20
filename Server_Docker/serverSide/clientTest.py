import socket
from Aplication.Client.ClientSockClass import *
from Server_Docker.server.requests import Request, ConstantsManagement


sock = ClientSocket(socket.gethostbyname(socket.gethostname()))
sock.connect()
request = Request(rq_type=ConstantsManagement.GETTICKETS.value, rq_data=None, client_token="a7cdf5d0586b392473dd0cd08c9ba833240006a8a7310bf9bc8bf1aefdfaeadb")
rq_json = request.to_json()

msg_len = len(rq_json)
send_len = str(msg_len).encode(ConstantsManagement.FORMAT.value)
send_len += b' ' * (ConstantsManagement.MAX_PKT_SIZE.value - len(send_len))
sock.client_socket.send(send_len)
sock.client_socket.send(rq_json.encode(ConstantsManagement.FORMAT.value))
msg_len =sock.client_socket.recv(ConstantsManagement.MAX_PKT_SIZE.value).decode(ConstantsManagement.FORMAT.value)
msg = sock.client_socket.recv(int(msg_len)).decode(ConstantsManagement.FORMAT.value)

sock.end()


print(msg)
