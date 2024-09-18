import sys

from Server.RouteClass import Route

sys.path.append('..')
from Server.utils import *
from Client.RequestsClass import *
from Client.ClientSockClass import *
from Server.ResponseClass import Response


MAX_SIZE_TRANSFER = 64
ENCOD = 'utf-8'
FAIL_CONNEXION = "erro de conexao"
TOKEN_NOT_DEFINED = "Usuario nao conectado"


def send_request(request, client:ClientSocket):

    print(request)
    if client.connect():
        size_transfer = str(len(request)).encode(ENCOD)
        size_transfer += b' ' * (MAX_SIZE_TRANSFER - len(size_transfer))
        client.client_socket.settimeout(5)
        try:
            client.client_socket.send(size_transfer)
            client.client_socket.send(request.encode(ENCOD))
            size_transfer = client.client_socket.recv(MAX_SIZE_TRANSFER)
            response_str = client.client_socket.recv(int(size_transfer.decode(ENCOD))).decode(ENCOD)
            print(response_str)
            server_response = Response()
            server_response.from_json(response_str)


            response = server_response

        except socket.error as e:
            response = Response(data={'execpt':str(e)}, rs_type=NETWORK_FAIL, status=NETWORK_ERROR)
            print(str(e))
        client.end()
    else:
        response = Response()
    return response


def buying(routes, client:ClientSocket):
    if client.token == '':
        return  0, TOKEN_NOT_DEFINED

    buy_request = Request(client_token=client.token, rq_data=[], rq_type=METHOD_BUY)

    for fligth in routes:
        route = Route()
        route.from_string(fligth)
        buy_request.rq_data.append(route.id)

    response = send_request(buy_request.to_json(), client)

    return response.status, response.data

def connect(email, client:ClientSocket):
    connect_request = Request(rq_data=email, rq_type=METHOD_GETTOKEN)
    response = send_request(connect_request.to_json(), client)

    return response.status, response.data


def search_routes(match, destination, client:ClientSocket):
    route_request = Request(client_token=client.token, rq_type=METHOD_GETROUTES, rq_data={'match':match, 'destination':destination})
    response = send_request(route_request.to_json(), client)
    print('chegou no buscar')
    return response.status, response.data


def create_account(email, client:ClientSocket):
    create_account_request = Request(rq_type=METHOD_CREATE_USER, rq_data=email)
    response = send_request(create_account_request.to_json(), client)

    return response.status, response.data

def search_bougths(client:ClientSocket):
    if client.token == '':
        return  0, TOKEN_NOT_DEFINED

    bougths_request = Request(client_token=client.token, rq_data=[], rq_type=METHOD_GETTICKETS)

    response = send_request(bougths_request.to_json(), client)

    return response.status, response.data