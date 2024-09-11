from Server.ServerClass import Server
from Server.ClientHandlerClass import ClientHandler
from threading import Thread, Lock
from Server.utils import DEFAULT_PORT
from socket import error

backlog_lock = Lock()

def process_client(client):   
    request = client.receive_pkt()
    client.send_pkt(request)
    #TODO:process request
    client.conn.close()
    with backlog_lock:
        Server.remove_client(client)


def main(port):
    server = Server()
    if not server.init_socket(port):
        exit(-1)
    
    while True:
        try:
            (conn, client) = server.server_socket.accept()
            new_client = ClientHandler(conn, client)
            Server.add_client(new_client)
            thread = Thread(target=process_client, args=(new_client,))
            thread.start()
        except error as er:
            print(f"[SERVER] Broken server. Error: {str(er)} Exiting!\n")
            return



# Select port #
port = int(input("Insert port value (0 for default): "))
port = port or DEFAULT_PORT
main(port)










