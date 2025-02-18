import webview
import os  # Add this import

class App:
    def send_message(self, message):
        from transmission.sender import MessageSender  # Move import here to avoid circular import

        return MessageSender.send_message(message)

    def send_signal(self, signal):
        from transmission.sender import MessageSender  # Move import here to avoid circular import

        return MessageSender.send_signal(signal)

    def receive_message(self):
        from transmission.receiver import MessageReceiver  # Move import here to avoid circular import

        return MessageReceiver.receive_message()

def main():
    app = App()
    script_dir = os.path.dirname(__file__)
    index_path = os.path.join(script_dir, 'index.html')
    window = webview.create_window('Data Pulse 2B1Q', index_path, width=1920, height=1080, js_api=app)
    webview.start()

if __name__ == '__main__':
    main()