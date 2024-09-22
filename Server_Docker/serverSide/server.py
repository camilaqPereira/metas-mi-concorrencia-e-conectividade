from serverSide.ClientHandlerClass import *
from serverSide.ServerClass import *
from server.requests import ConstantsManagement as cm
from DB.utils import ServerData
from concurrent.futures import ThreadPoolExecutor

def process_client(client:ClientHandler, server_data: ServerData):   
    print(f'init {client.addr}')

    try:
        request:Request = client.receive_pkt()
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


    except socket.error:
        client.conn.close()
        Server.remove_client(client)
        return
    
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
    Server.remove_client(client)
    
    return

def main(server_port):
    #Inicialização dos dados do servidor
    server_data = ServerData()
    #Inicialização do socket
    server = Server()

    if not server.init_socket(server_port):
        exit(-1)

    #Gerenciando conexões
    with ThreadPoolExecutor(max_workers=10) as exec:
        while True:
            try:
                (conn, client) = server.server_socket.accept()
                new_client = ClientHandler(conn, client)
                Server.add_client(new_client)
                exec.submit(process_client, new_client,server_data)
            except socket.error as er:
                print(f"[SERVER] Error accepting new connection. Error: {er} Retrying...\n")
            except KeyboardInterrupt:
                exit(-1)


# Select port #
port = 0 #int(input("Insert port value (0 for default): "))
port = port or ConstantsManagement.DEFAULT_PORT.value
main(port)