import socket
from re import match

import controller

ip = '127.0.0.1'

controller.conect(ip)

inicio = input("informe a sua origem: ")
destino = input("informe seu destino: ")

routes = controller.search_routes(match=inicio, destination=destino)

if routes['status']:
    i = 0
    for rota in routes['data'].keys():
        print(f"opcao {i}: {rota}")

    opc = input("digite o numero da rota desejada: ")

    response = controller.buying(opc)

    if response['status']:
        if response['status']['success']:
            print("compra bem sucedida")
        else:
            print("compra nao realizada")

elif routes['status'] == 0 and routes['raise']  == 0:
    print("dados para a rota nao encontrados")

else:
    print("houve uma excecao")


