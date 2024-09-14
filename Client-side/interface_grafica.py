
import sys
from time import sleep

from click import Tuple

from Server.RouteClass import Route
from Server.TicketClass import Ticket

sys.path.append('..')

from Server import utils
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
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    os.system(__CLEAR)
    match = input('digite de onde voce esta saindo:')
    destination = input('digite para onde voce deseja ir: ')

    (status, data) = controller.search_routes(match=match, destination=destination, client=client)
    color_list = ['\033[47;30m', '\033[49;0m']

    if  status == utils.OK:
        number_routes = len(data)

        i = 0

        opc = 0
        print('selecione uma das rotas: ')
        for flight in data:
            j=1
            color = color_list[0] if opc == i  else color_list[1]
            print(f'\t{color}rota {i+1}:\033[49;0m')
            for route in flight:
                path = Route()
                path.from_string(route)
                print(f'\t\tconexao {j}: {path.match} a {path.destination}')
                j+=1

            i+=1

        key = keyboard.read_event(True)

        while key.name != 'enter':
            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < number_routes:
                opc += 1
            else:
                pass

            os.system(__CLEAR)
            i = 0
            print('selecione uma das rotas: ')
            for flight in data:
                j = 1
                color = color_list[0] if opc == i else color_list[1]
                print(f'\t{color}rota {i + 1}:\033[49;0m')
                for route in flight:
                    path = Route()
                    path.from_string(route)
                    print(f'\t\tconexao {j}: {path.match} a {path.destination}')
                    j += 1

                i += 1

        (status, data) = controller.buying(routes=data[opc], client=client)

        if status == utils.OK:
            os.system(__CLEAR)
            ticket = Ticket()
            ticket.from_json(data)
            print("Compra efetuada com sucesso!")

            print(f"dados da compra:\n\temail: {ticket.email}\n\tdata: {ticket.timestamp}\n\tde {ticket.routes[0].match} "
                  f"a {ticket.routes[len(ticket.routes)-1].destination}")

            opc = 0
            print('Deseja salvar no computador ?')

            os.system(__CLEAR)
            print(f'{color_list[opc]}\tSim\033[49;0m')
            print(f'{color_list[1]}\tNao\033[49;0m')
            key = keyboard.read_event(True)

            while key.name != 'enter':
                if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                    opc -= 1
                elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                    opc += 1
                else:
                    pass

                os.system(__CLEAR)
                print(f'{color_list[opc*1]}\tSim\033[49;0m')
                print(f'{color_list[1-opc]}\tNao\033[49;0m')
                key = keyboard.read_event(True)
            #fazer gerar o coiso de arquivo


            print('pressione enter para retornar ao menu...')
            keyboard.wait('enter', True)
            menu(client=client)

        elif status == utils.OPERATION_FAILED:
            print('falha ao compra passagens, vaga indisponivel\nTente selecionar outra passagem')
            buy_route(client=client)

        else:
            print('falha na conexao')
            sleep(2)
            main_loop()

    elif status == utils.NOT_FOUND:
        print('Rotas escolhidas nao existem ou nao estao disponivel')
        menu(client)
    elif status == utils.OPERATION_FAILED:
        print('falha ao buscar rotas, deseja tentar novamente? ')
        opc = 0
        print(f'{color_line[0][opc]}\tSim\033[49;0m')
        print(f'{color_line[0][1]}\tNao\033[49;0m')
        key = keyboard.read_event(True)

        while key.name != 'enter':
            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                opc += 1
            else:
                pass

            os.system(__CLEAR)
            print('falha ao buscar rotas, deseja tentar novamente?')
            print(f'{color_line[0][opc * 1]}\tSim\033[49;0m')
            print(f'{color_line[0][1 - opc]}\tNao\033[49;0m')
            key = keyboard.read_event(True)

        if opc == 1:
            buy_route(client=client)
        else:
            menu(client)
    else:
        print('falha na conexao')
        main_loop()


def seek_bougths(client: ClientSocket):
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    os.system(__CLEAR)
    (status, data) = controller.search_bougths(client=client)

    if status == utils.OK:
        i = 0
        print('suas compras:')
        for ticket in data:
            print(f'compra {i+1}:\n\temail: {ticket.email}\n\tdata: {ticket.timestamp}\n\tSaida: {ticket.routes[0].match} '
                  f'a {ticket.routes[len(ticket.routes) - 1].destination}')
            i += 1

        print('pressione enter para retornar ao menu...')
        keyboard.wait('enter', True)
        menu(client=client)
    elif status == utils.NOT_FOUND:
        print('Nao existem comprar associadas a essa conta')
        print('\npressione enter para retornar ao menu...')
        keyboard.wait('enter', True)
        menu(client=client)
    elif status == utils.OPERATION_FAILED:
        print('falha ao buscar compras, deseja tentar novamente? ')
        opc = 0
        print(f'{color_line[0][opc]}\tSim\033[49;0m')
        print(f'{color_line[0][1]}\tNao\033[49;0m')
        key = keyboard.read_event(True)

        while key.name != 'enter':
            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                opc += 1
            else:
                pass

            os.system(__CLEAR)
            print('falha ao buscar compras, deseja tentar novamente?')
            print(f'{color_line[0][opc * 1]}\tSim\033[49;0m')
            print(f'{color_line[0][1 - opc]}\tNao\033[49;0m')
            key = keyboard.read_event(True)

        if opc == 1:
            seek_bougths(client=client)
        else:
            menu(client)
    else:
        print('falha na conexao')
        sleep(2)
        main_loop()

def submenu_status_ok(client: ClientSocket):
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    opc = 1
    os.system(__CLEAR)
    print('Selecione uma das opcoes abaixo: ')
    print(f'{color_line[opc - 1][0]}\t1 -> Comprar Passagem \033[49;0m')
    print(f'{color_line[opc - 1][1]}\t2 -> Consultar Compras\033[49;0m')
    print(f'{color_line[opc - 1][2]}\t3 -> Voltar\033[49;0m')

    key = keyboard.read_event(True)

    while key.name != '1' and key.name != '2' and key.name != '3' and key.name != 'enter':

        if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 1:
            opc -= 1
        elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 3:
            opc += 1
        else:
            pass

        os.system(__CLEAR)
        print('Selecione uma das opcoes abaixo: ')
        print(f'{color_line[opc - 1][0]}\t1 -> Comprar Passagem \033[49;0m')
        print(f'{color_line[opc - 1][1]}\t2 -> Consultar Compras\033[49;0m')
        print(f'{color_line[opc - 1][2]}\t3 -> Voltar\033[49;0m')
        key = keyboard.read_event(True)


    if key.name != 'enter':
        opc = int(key.name)

    if opc == 1:
        buy_route(client)
    elif opc == 2:
        seek_bougths(client)
    else:
        menu(client)
def submenu_status_token(client: ClientSocket, old_opc):
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    while True:
        opc = 0
        print('Usuario nao encontrado', end=', ')
        if old_opc == 2:
            print('deseja criar uma conta? ')
            print(f'{color_line[0][opc]}\tSim\033[49;0m')
            print(f'{color_line[0][1]}\tNao\033[49;0m')
            key = keyboard.read_event(True)

            while key.name != 'enter':
                if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                    opc -= 1
                elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                    opc += 1
                else:
                    pass

                os.system(__CLEAR)
                print('deseja criar uma conta? ')
                print(f'{color_line[0][opc * 1]}\tSim\033[49;0m')
                print(f'{color_line[0][1 - opc]}\tNao\033[49;0m')
                key = keyboard.read_event(True)

            if opc == 0:
                email = input('digite seu email: ')

                while email.find('@') == -1 or len(email) < 5:
                    email = input('por favor informe um email valido: ')

                (status, data) = controller.create_account(email, client)

                if status == utils.OK:
                    submenu_status_ok(client)
                elif status == utils.BAD_TOKEN:
                    pass
            else:
                while True:
                    os.system(__CLEAR)
                    print('escolha uma opcao:')
                    print(f'{color_line[0][opc]}\tTentar novamente\033[49;0m')
                    print(f'{color_line[0][1]}\tSair\033[49;0m')
                    key = keyboard.read_event(True)

                    while key.name != 'enter':
                        if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                            opc -= 1
                        elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                            opc += 1
                        else:
                            pass

                        os.system(__CLEAR)
                        print('escolha uma opcao:')
                        print(f'{color_line[0][opc * 1]}\tTentar novamente\033[49;0m')
                        print(f'{color_line[0][1 - opc]}\tSair\033[49;0m')
                        key = keyboard.read_event(True)

                    if opc == 0:
                        email = input('digite seu email: ')

                        while email.find('@') == -1 or len(email) < 5:
                            email = input('por favor informe um email valido: ')

                        (status, data) = controller.connect(email, client)

                        if status == utils.OK:
                            submenu_status_ok(client)
                        elif status == utils.BAD_TOKEN:
                            pass
                        elif status == utils.NOT_FOUND:
                            print('usuario nao encontrado')
                            submenu_create_account(client)
                        elif status == utils.OPERATION_FAILED:
                            print('conta ja existente\nPor favor fazer login')
                            submenu_login(client)
                        else:
                            print('falha na conexao, por favor tente novamente mais tarde')
                            sleep(2)
                            main_loop()
                    else:
                        exit(1)
        else:
            while True:
                os.system(__CLEAR)
                print('escolha uma opcao:')
                print(f'{color_line[0][opc]}\tTentar novamente\033[49;0m')
                print(f'{color_line[0][1]}\tSair\033[49;0m')
                key = keyboard.read_event(True)

                while key.name != 'enter':
                    if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                        opc -= 1
                    elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                        opc += 1
                    else:
                        pass

                    os.system(__CLEAR)
                    print('escolha uma opcao:')
                    print(f'{color_line[0][opc * 1]}\tTentar novamente\033[49;0m')
                    print(f'{color_line[0][1 - opc]}\tSair\033[49;0m')
                    key = keyboard.read_event(True)

                if opc == 0:
                    email = input('digite seu email: ')

                    while email.find('@') == -1 or len(email) < 5:
                        email = input('por favor informe um email valido: ')

                    (status, data) = controller.connect(email, client)

                    if status == utils.OK:
                        submenu_status_ok(client)
                    elif status == utils.BAD_TOKEN:
                        pass
                    elif status == utils.NOT_FOUND:
                        print('usuario nao encontrado')
                        submenu_create_account(client)
                    elif status == utils.OPERATION_FAILED:
                        print('conta ja existente\nPor favor fazer login')
                        submenu_login(client)
                    else:
                        print('falha na conexao, por favor tente novamente mais tarde')
                        sleep(2)
                        main_loop()
                else:
                    exit(1)
def submenu_login(client: ClientSocket):
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    opc = 0
    os.system(__CLEAR)

    print('escolha uma opcao:')
    print(f'{color_line[0][opc]}\tFazer Login\033[49;0m')
    print(f'{color_line[0][1]}\tSair\033[49;0m')
    key = keyboard.read_event(True)

    while key.name != 'enter':
        if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
            opc -= 1
        elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
            opc += 1
        else:
            pass

        os.system(__CLEAR)
        print('escolha uma opcao:')
        print(f'{color_line[0][opc * 1]}\tFazer Login\033[49;0m')
        print(f'{color_line[0][1 - opc]}\tSair\033[49;0m')
        key = keyboard.read_event(True)

    if opc == 0:
        email = input('digite seu email: ')

        while email.find('@') == -1 or len(email) < 5:
            email = input('por favor informe um email valido: ')

        (status, data) = controller.connect(email, client)

        if status == utils.OK:
            submenu_status_ok(client)
        elif status == utils.BAD_TOKEN:
            submenu_status_token(client, 2)
        elif status == utils.NOT_FOUND:
            print('usuario nao encontrado')
            submenu_create_account(client)
        elif status == utils.OPERATION_FAILED:
            print('conta ja existente\nPor favor fazer login')
            submenu_login(client)
        else:
            print('falha na conexao, por favor tente novamente mais tarde')
            sleep(2)
            main_loop()
    else:
        exit(1)
def submenu_create_account(client: ClientSocket):
    opc = 0
    color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                  ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                  ['\033[49;0m', '\033[49;0m', '\033[47;30m']]
    print('deseja criar uma conta? ')
    print(f'{color_line[0][opc]}\tSim\033[49;0m')
    print(f'{color_line[0][1]}\tNao\033[49;0m')
    key = keyboard.read_event(True)

    while key.name != 'enter':
        if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
            opc -= 1
        elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
            opc += 1
        else:
            pass

        os.system(__CLEAR)
        print('deseja criar uma conta? ')
        print(f'{color_line[0][opc * 1]}\tSim\033[49;0m')
        print(f'{color_line[0][1 - opc]}\tNao\033[49;0m')
        key = keyboard.read_event(True)

    if opc == 0:
        email = input('digite seu email: ')

        while email.find('@') == -1 or len(email) < 5:
            email = input('por favor informe um email valido: ')

        (status, data) = controller.create_account(email, client)

        if status == utils.OK:
            submenu_status_ok(client)
        elif status == utils.BAD_TOKEN:
            submenu_status_token(client, 1)
        elif status == utils.NOT_FOUND:
            print('usuario nao encontrado')
            submenu_create_account(client)
        elif status == utils.OPERATION_FAILED:
            print('conta ja existente\nPor favor fazer login')
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
        opc = 1
        color_line = [['\033[47;30m', '\033[49;0m', '\033[49;0m'],
                      ['\033[49;0m', '\033[47;30m', '\033[49;0m'],
                      ['\033[49;0m', '\033[49;0m', '\033[47;30m']]

        print('Selecione uma das opcoes abaixo: ')
        print(f'{color_line[opc - 1][0]}\t1 -> Criar conta \033[49;0m')
        print(f'{color_line[opc - 1][1]}\t2 -> Entrar\033[49;0m')
        print(f'{color_line[opc - 1][2]}\t3 -> Sair\033[49;0m')
        key = keyboard.read_event(True)

        while key.name != '1' and key.name != '2' and key.name != '3' and key.name != 'enter':

            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 1:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 3:
                opc += 1
            else:
                pass

            os.system(__CLEAR)
            print('Selecione uma das opcoes abaixo: ')
            print(f'{color_line[opc - 1][0]}\t1 -> Criar conta \033[49;0m')
            print(f'{color_line[opc - 1][1]}\t2 -> Entrar\033[49;0m')
            print(f'{color_line[opc - 1][2]}\t3 -> Sair\033[49;0m')
            key = keyboard.read_event(True)


        if key.name != 'enter':
            opc = int(key.name)
        if opc != 3:
            os.system(__CLEAR)
            email = input('digite seu email: ')

            while email.find('@') == -1 or len(email) < 5:
                email = input('por favor informe um email valido: ')

        if opc == 1:
            (status, data) = controller.create_account(email, client)
        elif opc == 2:
            (status, data) = controller.connect(email, client)
        else:
            exit(1)

        if status == utils.OK:
            submenu_status_ok(client=client)
        elif status == utils.BAD_TOKEN:
            submenu_status_token(client, opc)
        elif status == utils.NOT_FOUND:
            print('Nao foi possivel encontrar uma conta')
            submenu_create_account(client)
        elif status == utils.OPERATION_FAILED:
            print('conta ja existe\npor favor fazer login')
            submenu_login(client)
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


