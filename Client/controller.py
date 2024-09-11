import sys
from Client.RequestsClass import *
from Client.ClientSockClass import *
from Server.ResponseClass import Response


MAX_SIZE_TRANSFER = 64
ENCOD = 'utf-8'
FAIL_CONNEXION = "erro de conexao"
TOKEN_NOT_DEFINED = "Usuario nao conectado"


def send_request(request, client:ClientSocket):

    if client.connect():
        size_transfer = str(len(request)).encode(ENCOD)
        size_transfer += b' ' * (MAX_SIZE_TRANSFER - len(size_transfer))

        try:
            client.client_socket.send(size_transfer)
            client.client_socket.send(request.encode(ENCOD))
            size_transfer = client.client_socket.recv(MAX_SIZE_TRANSFER)

            server_response: Response = Response().from_json(client.client_socket.recv(int(size_transfer.decode(ENCOD))))

            if server_response.status == 0:
                response = {'status': 0, 'raise': 0}
            else:
                response = {'status': 1, 'data': server_response.data, 'ts':server_response.timestamp}

        except socket.error as e:
            response = {'status': 0, 'raise':1, 'execpt':str(e)}

        client.end()
    else:
        response = {'status': 0, 'raise': 2}
    return response


def buying(routes, client:ClientSocket):
    if client.token == '':
        return  0, TOKEN_NOT_DEFINED

    buy_request = Request(client_token=client.token, rq_data=[], rq_type="buy")

    for route in routes:
        buy_request.rq_data.append(route.id)

    response = send_request(buy_request.to_json(), client)

    if response['status']:
        if response['data']['status']:
            return 1, response['data']['id']
    elif response['status'] == 0 and response['raise'] == 0:
        return 0, "negada"
    else:
        return 0, FAIL_CONNEXION

def connect(email, client:ClientSocket):
    connect_request = Request(rq_data={'email':email}, rq_type='account_check')
    response = send_request(connect_request.to_json(), client)

    if response['status']:
        return 1, response['data']['user_id']
    else:
        if response['raise'] == 0:
            return 0, "id nao localizado"
        else:
            return 0, FAIL_CONNEXION


def search_routes(match, destination, client:ClientSocket):
    route_request = Request(client_token=client.token, rq_type='get_routes', rq_data={'match':match, 'destination':destination})
    response = send_request(route_request.to_json(), client)

    if response['status']:
        return 1, response['data']
    elif response['raise'] == 0:
        return 0, "nenhuma rota encontrada"
    else:
        return 0, FAIL_CONNEXION


def create_account(email, client:ClientSocket):
    create_account_request = Request(rq_type='create_account', rq_data={'email':email})
    response = send_request(create_account_request.to_json(), client)

    if response['status']:
        client_id = response['data']['user_id']
        connect(email, client)
        return 1, response['data']['user_id']
    elif response['raise'] == 0:
        return 0, "email ja cadastrado"
    else:
        return 0, FAIL_CONNEXION

def search_bougths(client:ClientSocket):
    if client.token == '':
        return  0, TOKEN_NOT_DEFINED

    bougths_request = Request(client_token=client.token, rq_data=[], rq_type='bougths')

    response = send_request(bougths_request.to_json(), client)

    if response['status']:
        return 1, response['data']
    elif response['raise'] == 0:
        return 0, "nenhuma compra encontrada"
    else:
        return 0, FAIL_CONNEXION