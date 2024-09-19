import sys
sys.path.append('..')

from Client import utils
from Client import controller
from Client.ClientSockClass import ClientSocket
from Client.requests import Ticket
from Client.utils import Route

ip = input("Digite o IP da maquina: ")

client = ClientSocket(ip=ip)

opc = int(input("1 pra criar conta e 2 para logar: "))
email = input("Informe seu email: ")
if opc == 1:
    (status, response) = controller.create_account(email, client)

    if status == utils.OK:
        print(f'ID do usuario: {response}')
        client.token = response
    else:
        print(response)

if opc == 2:
    (status, response) = controller.connect(email, client)

    if status == utils.OK:
        print('login realizado com sucesso')
        client.token = response
    else:
        print(response)

inicio = input("informe a sua origem: ")
destino = input("informe seu destino: ")

(status, routes) = controller.search_routes(match=inicio, destination=destino, client=client)

if status == utils.OK:
    i = 1

    for fligth in routes:
        print(f"opcao {i}:")
        j = 1

        for route in fligth:
            path = Route().from_string(route)
            print(f'\t conexão {j}: {path.match} a {path.destination}')
            j+=1

        i += 1

    opc = int(input("\n\ndigite o numero da rota desejada: "))

    (status, response) = controller.buying(routes=routes[opc - 1], client=client)

    if status == utils.OK:
        ticket = Ticket().from_json(response)
        print(f"compra aprovada, id: {response}")
    else:
        print(response)

else:
    print(routes)



