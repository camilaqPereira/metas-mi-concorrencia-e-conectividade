import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from Server.ServerClass import Server
from Server.ClientHandlerClass import ClientHandler
from threading import Thread, Lock
from Server.utils import *
from socket import error
from DB.routes import *


backlog_lock = Lock()



def process_client(client:ClientHandler, matches_and_destinations:list, flights:dict, routes_graph:Graph):   
    request = client.receive_pkt()
    if not request:
        return_data = (NETWORK_ERROR, None, NO_DATA_TYPE)
    elif request.rq_type == METHOD_CREATE_USER:
        return_data = client.create_user(request.rq_data)
    elif request.rq_type == METHOD_GETTOKEN:
        return_data = client.get_token(request.rq_data)
    elif request.rq_type == METHOD_GETROUTES:
        if client.validate_token(token=request.client_token):
            return_data = client.find_routes(routes_graph, matches_and_destinations, flights, request.rq_data['match'], request.rq_data['destination'])
        else:
            return_data = (BAD_TOKEN, None, NO_DATA_TYPE)    
    elif request.rq_type == METHOD_BUY:
        if client.validate_token(token=request.client_token):
            return_data = client.buy_routes(request.client_token, routes_graph, matches_and_destinations, flights, request.rq_data)
        else:
            return_data = (BAD_TOKEN, None, NO_DATA_TYPE)
    elif request.rq_type == METHOD_GETTICKETS:
        if client.validate_token(token=request.client_token):
            return_data = client.get_tickets(request.client_token)
        else:
            return_data = (BAD_TOKEN, None, NO_DATA_TYPE)
    else:
        return_data = (OPERATION_FAILED, None, NO_DATA_TYPE)

    client.send_pkt(return_data)
    client.conn.close()

    with backlog_lock:
        Server.remove_client(client)


def main(server_port):
    routes_graph = init_graph()
    matches_and_destinations, flights = upload_routes_data()

    server = Server()
    if not server.init_socket(server_port):
        exit(-1)
    
    while True:
        try:
            (conn, client) = server.server_socket.accept()
            new_client = ClientHandler(conn, client)
            with backlog_lock:
                Server.add_client(new_client)
            thread = Thread(target=process_client, args=(new_client,routes_graph, matches_and_destinations, flights, routes_graph))
            thread.start()
        except error as er:
            print(f"[SERVER] Server isn't accepting new connections. Error: {str(er)} Exiting!\n")
            return



# Select port #
port = 0 #int(input("Insert port value (0 for default): "))
port = port or DEFAULT_PORT
main(port)










