import unittest
import threading
import time
from transmission import *
from tests import Logger

class TestMessageTransmission(unittest.TestCase):
    logger = Logger().get_logger()
    host = 'localhost'
    port = 12345

    def setUp(self):
        self.message = "Olá, mundo! Teste áàãâéè~eêíìî~iõóòôúù~uûüïöëäç!@#$%¨&*()_+{`^}?:><-=[]~´/;.,°ºª¬¢£³²¹\"\'' 0123456789"
        self.logger.info(f"Message to send: {self.message}")
        self.receiver_thread = threading.Thread(target=self.start_receiver)
        self.receiver_thread.start()
        time.sleep(1)  # Give the receiver some time to start

    def start_receiver(self):
        self.received_message = MessageReceiver.receive_message(self.host, self.port)

    def send_message(self):
        signal = MessageSender.prepare_message(self.message)
        MessageSender.send_signal(signal['encoded_message'], self.host, self.port)

    def test_message_transmission(self):
        sender_thread = threading.Thread(target=self.send_message)
        sender_thread.start()

        # Create a data stream for the animation
        data_stream = [(i, i % 10) for i in range(20)]

        sender_thread.join()
        self.receiver_thread.join()
        self.assertEqual(self.message, self.received_message['message'])

    def tearDown(self):
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()