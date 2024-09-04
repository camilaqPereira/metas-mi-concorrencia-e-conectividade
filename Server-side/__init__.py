import socket
import threading
import time

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECTED"

#cria um socket ipv4  tcp/ip
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#encerra o socket caso o programa seja encerrado
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#deixa o server aberto
serv_socket.bind(ADDR)

def handle_client(con, addr):
    print("[SERVER] New connection\n")
    connected = True

    while connected:
        msg_size = con.recv(HEADER).decode(FORMAT)
        if msg_size:
            msg_size = int(msg_size)
            msg = con.recv(msg_size).decode(FORMAT)

            if msg  == DISCONNECT_MSG:
                connected = False

            print(f"[SERVER]: Message received {con} -> {msg}")
    
    con.close()
    
        

def start():
    serv_socket.listen(5)
    while True:
        (con, client) = serv_socket.accept()
        thread = threading.Thread(target=handle_client, args=(con, client))
        thread.start()
        print(f"[SERVER] Active threads {threading.activeCount() - 1}")



print('[SERVER] Server started\n')
start()


