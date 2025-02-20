import asyncio
import os
import webview

from transmission import *

"""
Classe da interface gráfica do usuário.
"""
class App:
    """
    Inicia a aplicação.
    """
    def __init__(self):
        self.received_message = None

    """
    Prepara a mensagem.
    """
    def prepare_message(self, message):
        return MessageSender.prepare_message(message)


    """
    Envia um sinal.
    """
    def send_signal(self, signal, host, port):
        return MessageSender.send_signal(signal, host, port)

    """
    Recebe uma mensagem.
    """
    def receive_message(self, conn):
        message = MessageReceiver.receive_message(conn)
        if message:
            self.set_received_message(message)
            asyncio.run(self.delay_message_processing())
            MessageReceiver.show_message_received()
        return message

    """
    Atrasa o processamento da mensagem para evitar conflitos.
    """
    async def delay_message_processing(self):
        await asyncio.sleep(3)

    """
    Define a mensagem recebida.
    """
    def set_received_message(self, message):
        self.received_message = message

    """
    Obtém a mensagem recebida.
    """
    def get_received_message(self):
        return self.received_message

    """
    Inicia a aplicação.
    """
    def run(self):
        script_dir = os.path.dirname(__file__)
        index_path = os.path.join(script_dir, 'index.html')
        window = webview.create_window('Team Data Pulse - 2B1Q', index_path, width=1050, height=775, js_api=self)
        webview.start()
