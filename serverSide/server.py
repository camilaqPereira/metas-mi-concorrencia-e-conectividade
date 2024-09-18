from serverSide.ClientHandlerClass import *
from serverSide.ServerClass import *
from Server.requests import ConstantsManagement
from DB.utils import ServerData
from threading import Thread, Lock

backlog_lock = Lock()

def process_client(client:ClientHandler, server_data: ServerData):   
    request = client.receive_pkt()
    if not request:
        return_data = (ConstantsManagement.NETWORK_ERROR.value, None, ConstantsManagement.NO_DATA_TYPE.value)
    elif request.rq_type == ConstantsManagement.CREATE_USER.value:
        return_data = client.create_user(request.rq_data)
    elif request.rq_type == ConstantsManagement.GETTOKEN.value:
        return_data = client.get_token(request.rq_data)
    elif request.rq_type == ConstantsManagement.GETROUTES.value:
        if client.auth_token(token=request.client_token):
            return_data = client.find_routes(server_data, request.rq_data['match'], request.rq_data['destination'])
        else:
            return_data = (ConstantsManagement.INVALID_TOKEN.value, None, ConstantsManagement.NO_DATA_TYPE.value)
    elif request.rq_type == ConstantsManagement.BUY.value:
        if client.auth_token(token=request.client_token):
            return_data = client.buy_routes(server_data, request.client_token, request.rq_data)
        else:
            return_data = (ConstantsManagement.INVALID_TOKEN.value, None, ConstantsManagement.NO_DATA_TYPE.value)
    elif request.rq_type == ConstantsManagement.GETTICKETS.value:
        if client.auth_token(token=request.client_token):
            return_data = client.get_tickets(request.client_token)
        else:
            return_data = (ConstantsManagement.INVALID_TOKEN.value, None, ConstantsManagement.NO_DATA_TYPE.value)
    else:
        return_data = (ConstantsManagement.OPERATION_FAILED.value, None, ConstantsManagement.NO_DATA_TYPE.value)

    client.send_pkt(return_data)
    client.conn.close()

    with backlog_lock:
        Server.remove_client(client)

def main(server_port):
    server_data = ServerData()
    server = Server()
    if not server.init_socket(server_port):
        exit(-1)
    
    while True:
        try:
            (conn, client) = server.server_socket.accept()
            new_client = ClientHandler(conn, client)
            with backlog_lock:
                Server.add_client(new_client)
            thread = Thread(target=process_client, args=(new_client,server_data))
            thread.start()
        except socket.error as er:
            print(f"[SERVER] Server isn't accepting new connections. Error: {str(er)} Exiting!\n")
            return



# Select port #
port = 0 #int(input("Insert port value (0 for default): "))
port = port or ConstantsManagement.DEFAULT_PORT.value
main(port)