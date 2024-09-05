import socket
import pickle
import sys
from array import ArrayType

from flask import request

from RequestsClass import *
from Server.RouteClass import *
from ClientSockClass import *

IP = ""
MAX_SIZE_TRANSFER = 64
ENCOD = 'utf-8'

client = ClientSocket()


def send_request(request):

    if client.connect(IP):
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


def buying(routes, client_id):
    request = BuyRequest(client_token=client_id)
    for route in routes:
        request.route.append(route.id)

    response = send_request(request)

    return response


def conect(ip, email):
    IP = ip
    request = AccountCheck(email)
    response = send_request(request)

    return response


def search_routes(match, destination, client_id):
    request = RouteRequest(match=match, destination=destination, client_token=client_id)
    response = send_request(request)

    return response

def create_account(email, ip):
    request = AccountCreate(email)
    response = send_request(request)

    if response['status']:
        client_id = response['data']
        conect(ip, email)
    return response

def search_bougths(client_token):
    request = BoughtRequest(client_token)

    response = send_request(request)

    return response