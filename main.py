import asyncio
import configparser
import json
import netifaces
import os
import socket
import threading
import websockets

from gui import App
from tests import Logger

logger_instance = Logger()
logger = logger_instance.get_logger()

# Endereço IP do aptador conectado à rede, do computador
ip = None

"""
Obtém o endereço IPv4 da conexão atual da máquina.
"""
def get_local_ip():
    if ip is not None:
        return ip
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            ipv4_info = addresses[netifaces.AF_INET][0]
            gateway = netifaces.gateways().get('default', {}).get(netifaces.AF_INET)
            if gateway and gateway[1] == interface:
                return ipv4_info['addr']
    return None

"""
Lê o arquivo de configuração.
"""
def read_config():
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(__file__)
    relative_path = os.path.join(script_dir, 'config.ini')
    config.read(relative_path)
    return config

"""
Gerenciador de eventos do WebSocket da interface gráfica do usuário.
"""
async def websocket_handler(websocket, path, app_instance):
    while True:
        if app_instance.message_changed:
            message = app_instance.get_received_message()
            if message:
                await websocket.send(json.dumps(message))
        await asyncio.sleep(1)

"""
Inicia o servidor de mensagens.
"""
def start_server(app_instance):
    config = read_config()
    host = get_local_ip()
    port = int(config['server']['port'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logger.info(f"Message server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            logger.info(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(conn, app_instance)).start()

"""
Lida com um cliente de mensagens.
"""
def handle_client(conn, app_instance):
    with conn:
        response = app_instance.receive_message(conn)

"""
Inicia o servidor de WebSocket da interface gráfica do usuário.
"""
async def start_websocket_server(app_instance):
    config = read_config()
    host = config['gui_server']['host']
    port = int(config['gui_server']['port'])
    # logger.info(f"Starting graphical user interface on {host}:{port}")
    start_server = websockets.serve(lambda ws, path: websocket_handler(ws, path, app_instance), host, port)
    await start_server

if __name__ == '__main__':
    app_instance = App()
    config = read_config()
    websocket_url = f"ws://{config['gui_server']['host']}:{config['gui_server']['port']}"
    app_instance.set_websocket_url(websocket_url)
    server_thread = threading.Thread(target=start_server, args=(app_instance,))
    server_thread.daemon = True
    server_thread.start()

    websocket_thread = threading.Thread(target=lambda: asyncio.run(start_websocket_server(app_instance)))
    websocket_thread.daemon = True
    websocket_thread.start()

    app_instance.run()
