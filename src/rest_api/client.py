import socket


host = socket.gethostname()  # as both code is running on same pc
port = 5000
client_socket = None

class DollyClient():
    name = "Dolly"
    
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((host, port))  # connect to the server
    
    
    def query_dolly(self, prompt):
        self.client_socket.send(prompt.encode())
        data = self.client_socket.recv(10240).decode()  # receive response
        return data
    
