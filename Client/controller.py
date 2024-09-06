
import sys
from RequestsClass import *
from ClientSockClass import *

CURRENT_IP = ""
MAX_SIZE_TRANSFER = 64
ENCOD = 'utf-8'
FAIL_CONNEXION = "erro de conexao"



def send_request(request, client:ClientSocket):

    if client.connect(CURRENT_IP):
        size_transfer = str(sys.getsizeof(request))
        size_transfer += ' ' * (MAX_SIZE_TRANSFER - sys.getsizeof(request))

        try:
            client.client_socket.send(size_transfer.encode(ENCOD))
            client.client_socket.send(request)
            size_transfer = client.client_socket.recv(1024)
            server_response = client.client_socket.recv(int(size_transfer.decode(ENCOD)))

            if int(size_transfer.decode(ENCOD)) == -1:
                response = {'status': 0, 'raise': 0}
            else:
                response = {'status': 1, 'data': server_response}

        except socket.error as e:
            response = {'status': 0, 'raise':1, 'execpt':str(e)}

        client.end()
    else:
        response = {'status': 0, 'raise': 2}
    return response


def buying(routes, client:ClientSocket):
    buy_request = BuyRequest(client_token=client.token)
    for route in routes:
        buy_request.route.append(route.id)

    response = send_request(buy_request, client)

    if response['status']:
        if response['data']['status']:
            return 1, response['data']['id']
    elif response['status'] == 0 and response['raise'] == 0:
        return 0, "negada"
    else:
        return 0, FAIL_CONNEXION

def connect(email, client:ClientSocket):
    connect_request = AccountCheck(email)
    response = send_request(connect_request, client)

    if response['status']:
        return 1, response['data']['user_id']
    else:
        if response['raise'] == 0:
            return 0, "id nao localizado"
        else:
            return 0, FAIL_CONNEXION


def search_routes(match, destination, client:ClientSocket):
    route_request = RouteRequest(match=match, destination=destination, client_token=client.token)
    response = send_request(route_request, client)

    if response['status']:
        return 1, response['data']
    elif response['raise'] == 0:
        return 0, "nenhuma rota encontrada"
    else:
        return 0, FAIL_CONNEXION


def create_account(email, client:ClientSocket):
    create_account_request = AccountCreate(email)
    response = send_request(create_account_request, client)

    if response['status']:
        client_id = response['data']['user_id']
        connect(email, client)
        return 1, response['data']['user_id']
    elif response['raise'] == 0:
        return 0, "email ja cadastrado"
    else:
        return 0, FAIL_CONNEXION

def search_bougths(client:ClientSocket):
    bougths_request = BoughtRequest(client.token)

    response = send_request(bougths_request, client)

    if response['status']:
        return 1, response['data']
    elif response['raise'] == 0:
        return 0, "nenhuma compra encontrada"
    else:
        return 0, FAIL_CONNEXION

    return response