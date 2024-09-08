import socket

IP = socket.gethostbyname(socket.gethostname())
HEADER = 64
PORT = 8000
ADDR = (IP,PORT)
FORMAT = "utf-8"



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

msg = input('digite sua mensagem: ')
msg_len = len(msg)
send_len = str(msg_len).encode(FORMAT)
send_len += b' ' * (HEADER - len(send_len))
client_socket.send(send_len)
client_socket.send(msg.encode('utf-8'))
msg_len = client_socket.recv(64).decode(FORMAT)
msg = client_socket.recv(int(msg_len)).decode(FORMAT)

client_socket.close()

print(f"Msg received: {msg}")