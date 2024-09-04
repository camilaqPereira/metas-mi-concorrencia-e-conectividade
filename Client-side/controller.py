import socket

from ClientSockClass import *

IP = ""

client = ClientSocket()


def send_request(request):

    client.connect(IP)
    size_transfer = len(request)


    try:
        client.client_socket.send(f'{size_transfer}'.encode('utf-8'))
        client.client_socket.send(request)
        size_transfer = client.client_socket.recv(1024)
        server_response = client.client_socket.recv(int(size_transfer.decode('utf-8')))

        if int(size_transfer.decode('utf-8')) == -1:
            response = {'status': 0, 'raise':'data not found'}
        else:
            response = {'status': 1, 'data': server_response}

    except socket.error as e:
        response = {'status': 0, 'raise':str(e)}

    client.end()
    return response


def buying(routes):
    request = f"buy|{routes}"
    response = send_request(request)

    return response


def conect(ip):
    IP = ip


def search_routes(match, destination):
    request = f"routes|{match}|{destination}"
    response = send_request(request)

    return response
