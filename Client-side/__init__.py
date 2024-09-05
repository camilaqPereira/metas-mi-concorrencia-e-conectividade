from Client import controller
from Client.controller import create_account, conect, client

ip = '127.0.0.1'

client_token = ''

opc = int(input("1 pra criar conta e 2 para logar: "))
email = input("Informe seu email: ")
if opc == 1:
    response = create_account(email, ip)

    if response['status']:
        print(f'ID do usuario: {response['data']}')
        client_token = response['data']
    else:
        print('falha ao criar usuario')

if opc == 2:
    response = conect(ip, email)

    if response['status']:
        print('login realizado com sucesso')
        client_token = response['data']
    else:
        print('erro ao loggar')

inicio = input("informe a sua origem: ")
destino = input("informe seu destino: ")

routes = controller.search_routes(match=inicio, destination=destino, client_id=client_token)

if routes['status']:
    i = 1
    for route in routes['data']:
        print(f"opcao {i}: trechos: ")

        for fligth in route:
            print(f'{fligth.match} a {fligth.destination}')

        i += 1

    opc = int(input("digite o numero da rota desejada: "))

    response = controller.buying(routes['data'][opc], client_id=client_token)

    if response['status']:
        if response['status']['success']:
            print("compra bem sucedida")
        else:
            print("compra nao realizada")

elif routes['status'] == 0 and routes['raise']  == 0:
    print("dados para a rota nao encontrados")

else:
    print("houve uma excecao")


