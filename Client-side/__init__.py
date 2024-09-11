import sys
sys.path.append('..')

from Client import controller
from Client.ClientSockClass import ClientSocket

ip = input("Digite o IP da maquina: ")

client = ClientSocket(ip=ip)

opc = int(input("1 pra criar conta e 2 para logar: "))
email = input("Informe seu email: ")
if opc == 1:
    (status, response) = controller.create_account(email, client)

    if status:
        print(f'ID do usuario: {response}')
        client.token = response
    else:
        print(response)

if opc == 2:
    (status, response) = controller.connect(email, client)

    if status:
        print('login realizado com sucesso')
        client.token = response
    else:
        print(response)

inicio = input("informe a sua origem: ")
destino = input("informe seu destino: ")

(status, routes) = controller.search_routes(match=inicio, destination=destino, client=client)

if status:
    i = 1
    for route in routes:
        print(f"opcao {i}: trechos: ")

        for fligth in route:
            print(f'\t => {fligth.match} a {fligth.destination}')

        i += 1

    opc = int(input("\n\ndigite o numero da rota desejada: "))

    (status, response) = controller.buying(routes=routes[opc - 1], client=client)

    if status:
        print(f"compra aprovada, id: {response}")
    else:
        print(response)

else:
    print(routes)



