#!/usr/bin/env python

import sys
from gui import create_gui

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <gui/send/receive> [mensagem]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "gui":
        create_gui()
    elif action == "send":
        if len(sys.argv) < 3:
            print("Uso: python main.py send <mensagem>")
            sys.exit(1)
        message = sys.argv[2]
        from sender import send_message
        send_message(message)
    elif action == "receive":
        from receiver import receive_message
        receive_message()
    else:
        print("Ação desconhecida. Use 'gui', 'send' ou 'receive'.")
        sys.exit(1)

if __name__ == "__main__":
    main()