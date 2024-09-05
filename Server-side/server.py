import socket
import threading

FORMAT = "utf-8"
HEADER = 64 #numero de bytes a serem recebidos na primeira mensagem
PORT = 8000
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)

#cria um socket ipv4 tcp/ip
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#encerra o socket caso o programa seja encerrado
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#deixa o server aberto
serv_socket.bind(ADDR)

#função para processamento de requisições
def handle_client(conn, addr):
    print("[SERVER] New connection\n")
    #recebendo primeiro pacote -> tamanho da mensagem
    try:
        msg_size = conn.recv(HEADER).decode(FORMAT)
        if msg_size:
            msg_size = int(msg_size)
            #recebendo segundo pacote -> mensagem
            msg = conn.recv(msg_size).decode(FORMAT)

        print(f"[SERVER]: Message received {addr} -> {msg}")
    except:
        print("[SERVER] Connection with client failed! Ending connection\n")
    conn.close()
    
def search_route_process():
    pass

def buy_route_process():
    pass



def start():
    serv_socket.listen(5)
    while True:
        (conn, client) = serv_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, client))
        thread.start()
        print(f"[SERVER] Active threads {threading.active_count() - 1}")


print('[SERVER] Server started\n')
start()


