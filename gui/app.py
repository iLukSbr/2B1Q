import webview
import os
import socket
from transmission import MessageSender, MessageReceiver

class App:
    def prepare_message(self, message):
        return MessageSender.prepare_message(message)

    def send_signal(self, signal, host, port):
        return MessageSender.send_signal(signal, host, port)

    def receive_message(self, conn):
        return MessageReceiver.receive_message(conn)

    def get_ip(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return {"ip": ip_address, "hostname": hostname}

    def run(self):
        script_dir = os.path.dirname(__file__)
        index_path = os.path.join(script_dir, 'index.html')
        window = webview.create_window('Team Data Pulse - 2B1Q', index_path, width=1300, height=600, js_api=self)
        webview.start()