from serverSide.ClientHandlerClass import *
from serverSide.ServerClass import *
from server.requests import ConstantsManagement as cm
from DB.utils import ServerData
from threading import Thread, Lock

def process_client(client:ClientHandler, server_data: ServerData, backlog_lock:Lock):   

    request:Request = client.receive_pkt()
    if not request:
        client.conn.close()
        with backlog_lock:
            Server.remove_client(client)
        return

    
    try:
        response:Response = Response()
        type = cm(request.rq_type).name

        if type != "CREATE_USER" and type != "GETTOKEN":
            client.auth_token(request.client_token)
        
        match type:
            case "CREATE_USER":
                response.data = client.create_user(request.rq_data) # type: ignore
                if response.data:
                    response.status = cm.OK
                    response.rs_type = cm.TOKEN_TYPE
                else:
                    response.status = cm.OPERATION_FAILED
                    response.rs_type = cm.NO_DATA_TYPE
            case "GETTOKEN":
                response.data = client.get_token(request.rq_data) # type: ignore
                response.status = cm.OK
                response.rs_type = cm.TOKEN_TYPE
            
            case "GETROUTES":
                response.data = server_data.search_route(request.rq_data['match'], request.rq_data['destination']) # type: ignore

                if response.data:
                    response.status = cm.OK
                    response.rs_type = cm.ROUTE_TYPE
                else:
                    response.status = cm.NOT_FOUND
                    response.rs_type = cm.NO_DATA_TYPE
            
            case "BUY":
                response.data = client.buy_routes(server_data, request.client_token, request.rq_data) # type: ignore

                if response.data:
                    response.status = cm.OK
                    response.rs_type = cm.TICKET_TYPE
                else:
                    response.status = cm.OPERATION_FAILED
                    response.rs_type = cm.NO_DATA_TYPE
            
            case "GETTICKETS":
                response.data = client.get_tickets(request.client_token)

                if response.data:
                    response.status = cm.OK
                    response.rs_type = cm.TICKET_TYPE
                else:
                    response.status = cm.NOT_FOUND
                    response.rs_type = cm.NO_DATA_TYPE
            
            case _:
                raise ValueError(f"[SERVER] {client.addr} No request type named {request.rq_type}")

    except InvalidTokenException:
        response.status = cm.INVALID_TOKEN
        response.data = None
        response.rs_type = cm.NO_DATA_TYPE

    except (KeyError, ValueError):
        response.status = cm.NOT_FOUND
        response.data = None
        response.rs_type = cm.NO_DATA_TYPE

    response.status = response.status.value
    response.rs_type = response.rs_type.value

    client.send_pkt(response)
    
    client.conn.close()
    with backlog_lock:
        Server.remove_client(client)


def main(server_port):
    #Inicialização dos dados do servidor
    server_data = ServerData()
    #Inicialização do mutex -> backlog de usuários 
    backlog_lock = Lock()
    #Inicialização do socket
    server = Server()

    if not server.init_socket(server_port):
        exit(-1)

    #Gerenciando conexões
    while True:
        try:
            (conn, client) = server.server_socket.accept()
            new_client = ClientHandler(conn, client)
            with backlog_lock:
                Server.add_client(new_client)
            thread = Thread(target=process_client, args=(new_client,server_data, backlog_lock))
            thread.start()
        except socket.error as er:
            print(f"[SERVER] Error accepting new connection. Error: {er} Retrying...\n")



# Select port #
port = 9000 #int(input("Insert port value (0 for default): "))
port = port or ConstantsManagement.DEFAULT_PORT.value
main(port)

