#!/usr/bin/env python

import unittest
import threading
import time
from transmission.sender import MessageSender
from transmission.receiver import MessageReceiver

class TestMessageTransmission(unittest.TestCase):
    def setUp(self):
        self.message = "Olá, mundo!"
        self.receiver_thread = threading.Thread(target=self.start_receiver)
        self.receiver_thread.start()
        time.sleep(1)  # Give the receiver some time to start

    def start_receiver(self):
        self.receiver = MessageReceiver()
        self.received_message = self.receiver.receive_message()

    def test_message_transmission(self):
        sender = MessageSender()
        sender.send_message(self.message)
        self.receiver_thread.join()
        self.assertEqual(self.message, self.received_message)

    def tearDown(self):
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()