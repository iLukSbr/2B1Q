#!/usr/bin/env python

from gui import App
import socket
import threading

def start_server(app_instance):
    host = 'localhost'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn, app_instance)).start()

def handle_client(conn, app_instance):
    with conn:
        response = app_instance.receive_message(conn)

if __name__ == '__main__':
    app_instance = App()
    server_thread = threading.Thread(target=start_server, args=(app_instance,))
    server_thread.daemon = True
    server_thread.start()

    app_instance.run()