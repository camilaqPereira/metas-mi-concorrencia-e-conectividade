import os

import keyboard

def ysno_menu(text: str, clear_str: str):
    opc = 0
    color_list = ['\033[47;30m', '\033[49;0m']
    while True:
        os.system(clear_str)
        print(text)
        print(f'{color_list[opc*1]}\tSim\033[49;0m')
        print(f'{color_list[1-opc]}\tNao\033[49;0m')
        key = keyboard.read_event(True)

        if key.name == 'enter':
            return opc
        else:
            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < 1:
                opc += 1
            else:
                pass

def enumerate_menu(text_opc: list[str], text: str, clear_str: str):
    opc = 0
    color_list = ['\033[47;30m', '\033[49;0m']


    while True:
        os.system(clear_str)
        print(text)
        for item in text_opc:
            print(f'{text_opc.index(item)+1}->{color_list[0] if opc == text_opc.index(item) else color_list[1]}\t{item}\033[49;0m')

        key = keyboard.read_event(True)

        if key.name == 'enter' and key.event_type == keyboard.KEY_DOWN:
            return opc
        else:
            if key.event_type == keyboard.KEY_DOWN and key.name == 'up' and opc > 0:
                opc -= 1
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'down' and opc < len(text_opc):
                opc += 1
            else:
                pass


