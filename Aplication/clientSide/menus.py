import os
from time import sleep

import keyboard

def ysno_menu(text: str, clear_str: str):
    opc = 0
    color_list = ['\033[47;30m', '\033[49;0m']
    while True:
        os.system(clear_str)
        print(text)
        print(f'{color_list[opc*1]}\t1 <- Sim\033[49;0m')
        print(f'{color_list[1-opc]}\t2 <- Nao\033[49;0m')

        opc = int(input('opção: ')) - 1
        if opc == 0 or opc == 1:
            return opc
        else:
            print('opção invalida!')
            sleep(2)

def enumerate_menu(text_opc: list, text: str, clear_str: str):
    color_list = ['\033[47;30m', '\033[49;0m']


    while True:
        opc = 0
        os.system(clear_str)
        print(text)
        for item in text_opc:
            print(f'{text_opc.index(item)+1} <- {color_list[0] if opc == text_opc.index(item) else color_list[1]}\t{item}\033[49;0m')

        opc = int(input('opção: ')) - 1
        if 0 <= opc < len(text_opc):
            return opc
        else:
            print('opção invalida!')
            sleep(2)


