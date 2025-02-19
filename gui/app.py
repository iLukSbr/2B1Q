import netifaces
import os
import socket
import webview
from transmission import *

class App:
    def __init__(self):
        self.received_message = None
        self.message_changed = False

    def prepare_message(self, message):
        return MessageSender.prepare_message(message)

    def send_signal(self, signal, host, port):
        return MessageSender.send_signal(signal, host, port)

    def receive_message(self, conn):
        message = MessageReceiver.receive_message(conn)
        if message:
            self.set_received_message(message)
        return message

    def set_received_message(self, message):
        self.received_message = message
        self.message_changed = True

    def get_received_message(self):
        self.message_changed = False
        return self.received_message

    # def get_ip(self):
    #     hostname = socket.gethostname()
    #     ip_address = self.get_active_ip()
    #     return f"{ip_address}:{hostname}"

    def run(self):
        script_dir = os.path.dirname(__file__)
        index_path = os.path.join(script_dir, 'index.html')
        window = webview.create_window('Team Data Pulse - 2B1Q', index_path, width=1300, height=1000, js_api=self)
        webview.start()