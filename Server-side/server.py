import sys

from Client.RequestsClass import Request
from Server.ResponseClass import Response
from Server.RouteClass import Route
from Server.TicketClass import Ticket

sys.path.append('..')

from Server.ServerClass import Server
from Server.ClientHandlerClass import ClientHandler
from threading import Thread, Lock
from Server.utils import DEFAULT_PORT
from socket import error
from Server import utils

backlog_lock = Lock()

def process_client(client):   
    request = client.receive_pkt()
    response = Response()

    if request.rq_type == utils.METHOD_CREATE_USER:
        response.status = utils.OK
        response.data = "user_maike_ok"
        response.rs_type = utils.TOKEN_TYPE
    elif request.rq_type == utils.METHOD_GETTOKEN:
        response.status = utils.OK
        response.data = "user_maike_ok"
        response.rs_type = utils.TOKEN_TYPE
    elif request.rq_type == utils.METHOD_GETROUTES:
        response.status = utils.OK
        response.data = [[Route('uruguai', 'bahia', 1, 'algo')],
                         [Route('uruguai', 'são paulo', 1, 'algo 2'), Route('são paulo', 'bahia', 1, 'algo 3')],
                         [Route('uruguai', 'são paulo', 1, 'algo 4'), Route('são paulo', 'rio de janeiro', 1, 'algo 3'), Route('rio de janeiro', 'bahia', 1, 'algo 4')]]
        response.rs_type = utils.ROUTE_TYPE

    elif request.rq_type == utils.METHOD_BUY:
        response.status = utils.OK
        response.data = Ticket('abobrinha',routes=request.rq_data)
        response.rs_type = utils.TICKET_TYPE
    elif request.rq_type == utils.METHOD_GETTICKETS:
        response.status = utils.OK
        response.data = [Ticket('abobrinha', routes=Route('Uruguai', 'venezuela', 1, 'algo'))]
        response.rs_type = utils.TICKET_TYPE

    client.send_pkt(response)
    client.conn.close()
    with backlog_lock:
        Server.remove_client(client)


def main(server_port):
    server = Server()
    if not server.init_socket(server_port):
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










