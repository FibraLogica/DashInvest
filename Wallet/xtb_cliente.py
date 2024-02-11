from .broker_connector import BrokerConnector
import json
import socket
import ssl
import environ

env = environ.Env()
environ.Env.read_env()

DEFAULT_XAPI_ADDRESS = 'xapi.xtb.com'
DEFAULT_XAPI_PORT_SSL = 5112

class XTBClient(BrokerConnector):
    def __init__(self, user_id = None, password=None, broker_name='XTB', address=DEFAULT_XAPI_ADDRESS, port=DEFAULT_XAPI_PORT_SSL):
        if user_id is None:
            user_id = env('XTB_USER_ID', default=None)
        if password is None:
            password = env('XTB_PASSWORD', default=None)
        if not user_id or not password:
            raise ValueError('XTB user_id and password must be provided or set as environment variables.')
        super().__init__(user_id, password, broker_name)
        self.address = address
        self.port = port
        self.sock = None
        self.user_id = user_id

    def connect(self):
        context = ssl.create_default_context()
        self.sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.address)
        self.sock.connect((self.address, self.port))
        print("Conectado ao servidor XTB.")

    def disconnect(self):
        if self.sock:
            self.sock.close()
            print("Desconectado do servidor XTB.")

    def login(self):
        response = self.send_command("login", {"userId": self.user_id, "password": self.password})
        return response

    def send_command(self, command, arguments):
        message = json.dumps({"command": command, "arguments": arguments}).encode('utf-8')
        self.sock.sendall(message)
        return self.receive_response()

    def get_margin_level(self):
        response = self.send_command("getMarginLevel", {})
        return response
    
    def get_current_user_data(self):
        response = self.send_command("getCurrentUserData", {})
        return response
    
    def get_current_user_symbols(self):
        response = self.send_command("getAllSymbols", {})
        return response

    def receive_response(self):
        response = b""
        while True:
            data = self.sock.recv(4096)
            response += data
            if len(data) < 4096:
                break
        return json.loads(response.decode('utf-8'))


