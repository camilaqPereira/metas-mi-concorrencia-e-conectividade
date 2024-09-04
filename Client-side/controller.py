from ClientSockClass import *

ip = ""

client = ClientSocket()


def send_request(request):
    response = {}
    size_transfer = len(request)
    client.client_socket.send(f'{size_transfer}'.encode('utf-8'))
    client.client_socket.send(request)
    size_transfer = client.client_socket.recv(1024)
    server_response = client.client_socket.recv(int(size_transfer.decode('utf-8')))

    if int(size_transfer.decode('utf-8')) == -1:
        response = {'status': False}
    else:
        response = {'status': True, 'data': server_response}

    return response


def buying(routes):
    request = f"buy|{routes}"
    response = send_request(request)

    return response


def conect(ip):
    client.connect(ip)


def search_routes(match, destination):
    request = f"routes|{match}|{destination}"
    response = send_request(request)

    return response
