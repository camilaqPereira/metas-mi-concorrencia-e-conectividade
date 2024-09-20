from time import sleep
from Client import requests
from Client import utils
from clientSide import menus
import keyboard
from Client import controller
import os
from Client.ClientSockClass import ClientSocket
from sys import platform

#checar o sistema que o codigo esta sendo rodado


if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
    __CLEAR = 'clear'
else:
    __CLEAR =  'cls'

def buy_route(client: ClientSocket):
    os.system(__CLEAR)
    match = input('digite de onde voce esta saindo:')
    destination = input('digite para onde voce deseja ir: ')

    (status, data) = controller.search_routes(match=match, destination=destination, client=client)
    color_list = ['\033[47;30m', '\033[49;0m']

    if  status == requests.ConstantsManagement.OK:
        number_routes = len(data)

        i = 0

        opc = 0
        while True:
            os.system(__CLEAR)
            i = 0
            print('selecione uma das rotas: ')
            for flight in data:
                j = 1
                color = color_list[0] if opc == i else color_list[1]
                print(f'\t{color}rota {i + 1}:\033[49;0m')
                for route in flight:
                    path = utils.Route()
                    path.from_string(route)
                    print(f'\t\tconexao {j}: {path.match} a {path.destination}')
                    j += 1

                i += 1
            key = keyboard.read_event(True)
            if key.event_type == keyboard.KEY_DOWN and key.name == 'enter':
                break
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < number_routes:
                opc += 1
            else:
                pass



        (status, data) = controller.buying(routes=data[opc], client=client)

        if status == requests.ConstantsManagement.OK:
            os.system(__CLEAR)
            ticket = requests.Ticket()
            ticket.from_json(data)
            print("Compra efetuada com sucesso!")

            print(f"dados da compra:\n\temail: {ticket.email}\n\tdata: {ticket.timestamp}\n\tde {ticket.routes[0].match} "
                  f"a {ticket.routes[len(ticket.routes)-1].destination}")

            print('pressione enter para retornar ao menu...')
            keyboard.wait('enter', True)
            menu(client=client)

        elif status == requests.ConstantsManagement.OPERATION_FAILED:
            print('falha ao compra passagens, vaga indisponivel\nTente selecionar outra passagem')
            sleep(2)
            buy_route(client=client)

        else:
            print('falha na conexao')
            sleep(2)
            main_loop()

    elif status == requests.ConstantsManagement.NOT_FOUND:
        print('Rotas escolhidas nao existem ou nao estao disponivel')
        menu(client)
    elif status == requests.ConstantsManagement.OPERATION_FAILED:
        opc = menus.ysno_menu('falha ao buscar rotas, deseja tentar novamente?', __CLEAR)

        if opc == 0:
            buy_route(client=client)
        else:
            menu(client)
    else:
        print(f"data = {data} e status = {status}")
        main_loop()


def seek_bougths(client: ClientSocket):
    color_list = ['\033[47;30m', '\033[49;0m']
    os.system(__CLEAR)
    (status, data) = controller.search_bougths(client=client)

    if status == requests.ConstantsManagement.OK:
        i = 0
        print('suas compras:')
        for ticket in data:
            print(f'compra {i+1}:\n\temail: {ticket.email}\n\tdata: {ticket.timestamp}\n\tSaida: {ticket.routes[0].match} '
                  f'a {ticket.routes[len(ticket.routes) - 1].destination}')
            i += 1

        print('pressione enter para retornar ao menu...')
        keyboard.wait('enter', True)
        menu(client=client)
    elif status == requests.ConstantsManagement.NOT_FOUND:
        print('Nao existem comprar associadas a essa conta')
        print('\npressione enter para retornar ao menu...')
        keyboard.wait('enter', True)
        menu(client=client)
    elif status == requests.ConstantsManagement.OPERATION_FAILED:
        print('falha ao buscar compras, deseja tentar novamente? ')
        opc = menus.ysno_menu('falha ao buscar compras, deseja tentar novamente? ', __CLEAR)


        if opc == 0:
            seek_bougths(client=client)
        else:
            menu(client)
    else:
        print('falha na conexao')
        sleep(2)
        main_loop()

def submenu_status_ok(client: ClientSocket):
    opc = menus.enumerate_menu(['Comprar Passagem', 'Consultar Compras', 'Voltar'], 'selecione uma das opcoes abaixo:', __CLEAR)
    if opc == 0:
        buy_route(client)
    elif opc == 1:
        seek_bougths(client)
    else:
        menu(client)
def submenu_status_token(client: ClientSocket, old_opc):
    color_list = ['\033[47;30m', '\033[49;0m']
    while True:
        opc = 0
        print('Usuario nao encontrado')
        if old_opc == 1:
            opc = menus.ysno_menu('deseja criar uma conta? ', __CLEAR)

            if opc == 0:
                email = input('digite seu email: ')

                while email.find('@') == -1 or len(email) < 5:
                    email = input('por favor informe um email valido: ')

                (status, data) = controller.create_account(email, client)

                if status == requests.ConstantsManagement.OK:
                    submenu_status_ok(client)
                elif status == requests.ConstantsManagement.INVALID_TOKEN:
                    pass
            else:
                while True:
                    opc = menus.enumerate_menu(['Tentar novamente', 'Sair'], 'Escolha uma opcao:', __CLEAR)

                    if opc == 0:
                        email = input('digite seu email: ')

                        while email.find('@') == -1 or len(email) < 5:
                            email = input('por favor informe um email valido: ')

                        (status, data) = controller.connect(email, client)

                        if status == requests.ConstantsManagement.OK:
                            submenu_status_ok(client)
                        elif status == requests.ConstantsManagement.INVALID_TOKEN:
                            pass
                        elif status == requests.ConstantsManagement.NOT_FOUND:
                            print('usuario nao encontrado')
                            sleep(2)
                            submenu_create_account(client)
                        elif status == requests.ConstantsManagement.OPERATION_FAILED:
                            print('conta ja existente\nPor favor fazer login')
                            sleep(2)
                            submenu_login(client)
                        else:
                            print('falha na conexao, por favor tente novamente mais tarde')
                            sleep(2)
                            main_loop()
                    else:
                        exit(1)
        else:
            while True:
                opc = menus.enumerate_menu(['Tentar novamente', 'Sair'], 'Escolha uma opcao:', __CLEAR)

                if opc == 0:
                    email = input('digite seu email: ')

                    while email.find('@') == -1 or len(email) < 5:
                        email = input('por favor informe um email valido: ')

                    (status, data) = controller.connect(email, client)

                    if status == requests.ConstantsManagement.OK:
                        submenu_status_ok(client)
                    elif status == requests.ConstantsManagement.INVALID_TOKEN:
                        pass
                    elif status == requests.ConstantsManagement.NOT_FOUND:
                        print('usuario nao encontrado')
                        sleep(2)
                        submenu_create_account(client)
                    elif status == requests.ConstantsManagement.OPERATION_FAILED:
                        print('conta ja existente\nPor favor fazer login')
                        sleep(2)
                        submenu_login(client)
                    else:
                        print('falha na conexao, por favor tente novamente mais tarde')
                        sleep(2)
                        main_loop()
                else:
                    exit(1)
def submenu_login(client: ClientSocket):
    opc = menus.enumerate_menu(['Fazer Login', 'Sair'], 'Selecione uma opcao:', __CLEAR)

    if opc == 0:
        email = input('digite seu email: ')

        while email.find('@') == -1 or len(email) < 5:
            email = input('por favor informe um email valido: ')

        (status, data) = controller.connect(email, client)

        if status == requests.ConstantsManagement.OK:
            submenu_status_ok(client)
        elif status == requests.ConstantsManagement.INVALID_TOKEN:
            submenu_status_token(client, 2)
        elif status == requests.ConstantsManagement.NOT_FOUND:
            print('usuario nao encontrado')
            sleep(2)
            submenu_create_account(client)
        elif status == requests.ConstantsManagement.OPERATION_FAILED:
            print('conta ja existente\nPor favor fazer login')
            sleep(2)
            submenu_login(client)
        else:
            print('falha na conexao, por favor tente novamente mais tarde')
            sleep(2)
            main_loop()
    else:
        exit(1)
def submenu_create_account(client: ClientSocket):
    opc = menus.ysno_menu('Deseja criar uma conta?', __CLEAR)
    if opc == 0:
        email = input('digite seu email: ')

        while email.find('@') == -1 or len(email) < 5:
            email = input('por favor informe um email valido: ')

        (status, data) = controller.create_account(email, client)

        if status == requests.ConstantsManagement.OK:
            submenu_status_ok(client)
        elif status == requests.ConstantsManagement.INVALID_TOKEN:
            submenu_status_token(client, 1)
        elif status == requests.ConstantsManagement.NOT_FOUND:
            print('usuario nao encontrado')
            sleep(2)
            submenu_create_account(client)
        elif status == requests.ConstantsManagement.OPERATION_FAILED:
            print('conta ja existente\nPor favor fazer login')
            sleep(2)
            submenu_login(client)
        else:
            print('falha na conexao, por favor tente novamente mais tarde')
            sleep(2)
            main_loop()
    else:
        main_loop()
def menu(client: ClientSocket):
    os.system(__CLEAR)
    while True:
        opc = menus.enumerate_menu(['Criar conta', 'Entrar', 'Sair'], 'Selecione uma das opcoes abaixo:', __CLEAR)

        email: str = ''

        if opc != 2:
            os.system(__CLEAR)
            email = input('digite seu email: ')

            while email.find('@') == -1 or len(email) < 5:
                email = input('por favor informe um email valido: ')

        if opc == 0:
            (status, data) = controller.create_account(email, client)
        elif opc == 1:
            (status, data) = controller.connect(email, client)
        else:
            exit(1)

        if status == requests.ConstantsManagement.OK:
            client.token = data
            submenu_status_ok(client=client)
        elif status == requests.ConstantsManagement.INVALID_TOKEN:
            submenu_status_token(client, opc)
        elif status == requests.ConstantsManagement.NOT_FOUND:
            print('Nao foi possivel encontrar uma conta')
            sleep(2)
            submenu_create_account(client)
        elif status == requests.ConstantsManagement.OPERATION_FAILED and opc == 0:
            print('conta ja existe\npor favor fazer login')
            sleep(2)
            submenu_login(client)
        elif  status == requests.ConstantsManagement.OPERATION_FAILED and opc == 1:
            print('conta nao existe\npor favor fazer criar conta')
            sleep(2)
            submenu_status_token(client, 1)
        else:
            print('falha na conexao, por favor tente novamente mais tarde')
            sleep(2)
            main_loop()


def main_loop():
    ip = input("Digite o IP do servidor: ")

    new_client = ClientSocket(ip=ip)


    if new_client.connect():
        os.system(__CLEAR)
        print('conexao estabelecida')
        sleep(2)
        new_client.end()
    else:
        os.system(__CLEAR)
        print('nao foi possivel conectar')
        exit(1)

    menu(new_client)

main_loop()


