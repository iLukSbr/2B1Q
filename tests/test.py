#!/usr/bin/env python

import unittest
import threading
import time
from transmission.sender import MessageSender
from transmission.receiver import MessageReceiver

class TestMessageTransmission(unittest.TestCase):
    def setUp(self):
        self.message = "Olá, mundo! Teste áàãâéè~eêíìî~iõóòôúù~uûüïöëäç!@#$%¨&*()_+{`^}?:><-=[]~´/;.,°ºª¬¢£³²¹\"\'' 0123456789"
        logger.debug(f"Message to send: {self.message}")
        self.receiver_thread = threading.Thread(target=self.start_receiver)
        self.receiver_thread.start()
        time.sleep(1)  # Give the receiver some time to start

    def start_receiver(self):
        self.receiver = MessageReceiver()
        self.received_message = self.receiver.receive_message()

    def test_message_transmission(self):
        sender = MessageSender()
        sender_response = sender.send_message(self.message)
        sender.send_signal(sender_response['encoded_message'])
        self.receiver_thread.join()
        self.assertEqual(self.message, self.received_message['message'])

    def tearDown(self):
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()