#!/usr/bin/env python3

import socket
import threading
import time
import unittest

from tests import Logger
from transmission import *

"""
Classe de teste de envio e recebimento de mensagens.
"""


class TestMessageTransmission(unittest.TestCase):
    logger = Logger().get_logger()
    host = 'localhost'
    port = 12345

    """
    Define a mensagem de teste a ser enviada.
    """

    def setUp(self):
        self.message = "Olá, mundo! Teste áàãâéè~eêíìî~iõóòôúù~uûüïöëäç!@#$%¨&*()_+{`^}?:><-=[]~´/;.,°ºª¬¢£³²¹\"\'' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ æøåÆØÅ ςερτυθιοπλκξηγφδσαζχψωβνμ ςΕΡΤΥΘΙΟΠΛΚΞΗΓΦΔΣΑΖΧΨΩΒΝΜ あいうえおはひふへほさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん ぁぃぅぇぉゃゅょっゎゐゑゔゕゖ゗゘゙゚゛゜ゝゞゟ゠ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ"
        self.logger.info(f"Message to send: {self.message}")

        # Create a socket and bind to the host and port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        self.receiver_thread = threading.Thread(target=self.start_receiver)
        self.receiver_thread.start()
        time.sleep(1)  # Give the receiver some time to start

    """
    Inicia o receptor de mensagens de teste.
    """

    def start_receiver(self):
        conn, _ = self.server_socket.accept()
        self.received_message = MessageReceiver.receive_message(conn)

    """
    Envia a mensagem de teste.
    """

    def send_message(self):
        signal = MessageSender.prepare_message(self.message)
        MessageSender.send_signal(signal['encoded_message'], self.host, self.port)

    """
    Testa a transmissão de mensagens.
    """

    def test_message_transmission(self):
        sender_thread = threading.Thread(target=self.send_message)
        sender_thread.start()

        data_stream = [(i, i % 10) for i in range(20)]

        sender_thread.join()
        self.receiver_thread.join()
        self.assertEqual(self.message, self.received_message['message'])

    """
    Limpa os recursos após o teste.
    """

    def tearDown(self):
        self.server_socket.close()


"""
Chama a função de teste.
"""
if __name__ == '__main__':
    unittest.main()
