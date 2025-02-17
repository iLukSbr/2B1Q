from flask import Flask, render_template, request, jsonify, send_file
from zeroconf import ServiceInfo, Zeroconf
import socket
from gui.graph import Graph
from transmission import *

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.received_message = ""
        self.received_signal = []
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/send', methods=['POST'])
        def send_message():
            message = request.form['message']
            print(f"Message to send: {message}")
            sender = Sender()
            signal = sender.send_message(message)  # Use Sender class to get the signal
            Graph.plot_voltage_time(signal, "Sender Signal", "static/sender_signal.png")
            return jsonify(status="Message sent")

        @self.app.route('/receive', methods=['GET'])
        def receive_message():
            receiver = Receiver()  # Use Receiver class to get the signal
            self.received_signal = receiver.receive_message()
            Graph.plot_voltage_time(self.received_signal, "Receiver Signal", "static/receiver_signal.png")
            return jsonify(message=self.received_message)

        @self.app.route('/graph/<role>')
        def get_graph(role):
            if role == "sender":
                return send_file("static/sender_signal.png", mimetype='image/png')
            elif role == "receiver":
                return send_file("static/receiver_signal.png", mimetype='image/png')
            else:
                return "Invalid role", 400

    def register_mdns_service(self):
        zeroconf = Zeroconf()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        service_info = ServiceInfo(
            "_http._tcp.local.",
            "MessageApp._http._tcp.local.",
            addresses=[socket.inet_aton(ip_address)],
            port=5000,
            properties={},
            server=f"{hostname}.local."
        )
        zeroconf.register_service(service_info)
        return zeroconf

    def run(self):
        zeroconf = self.register_mdns_service()
        try:
            self.app.run(host='0.0.0.0', port=5000)
        finally:
            zeroconf.unregister_all_services()
            zeroconf.close()