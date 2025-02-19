import asyncio
import configparser
import websockets
import json
import netifaces
import socket
import threading
from gui import App

def get_local_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ipv4_info = addresses[netifaces.AF_INET][0]
            return ipv4_info['addr']
    return None

async def websocket_handler(websocket, path, app_instance):
    while True:
        if app_instance.message_changed:
            message = app_instance.get_received_message()
            if message:
                await websocket.send(json.dumps(message))
        await asyncio.sleep(1)

def start_server(app_instance):
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = get_local_ip()
    port = int(config['server']['port'])

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

async def start_websocket_server(app_instance):
    start_server = websockets.serve(lambda ws, path: websocket_handler(ws, path, app_instance), "localhost", 6789)
    await start_server

if __name__ == '__main__':
    app_instance = App()
    server_thread = threading.Thread(target=start_server, args=(app_instance,))
    server_thread.daemon = True
    server_thread.start()

    websocket_thread = threading.Thread(target=lambda: asyncio.run(start_websocket_server(app_instance)))
    websocket_thread.daemon = True
    websocket_thread.start()

    app_instance.run()