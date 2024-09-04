import socket
import json
from ClientSockClass import *

ip = ""

client = ClientSocket(ip)

def send_request(request):
    size_transfer = len("request")
    client.client_socket.send(f'{size_transfer}'.encode('utf-8'))
    client.client_socket.send(request)
    size_transfer = client.client_socket.recv(1024)
    response = client.client_socket.recv(int(size_transfer.decode('utf-8')))

    return response

def buying(routes):
    #envia a solicitação de compra

def conect(ip):
    client.connect()

def search_routes(match, destination):
    #envia a solicitação de trechos
