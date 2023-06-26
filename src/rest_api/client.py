import socket


host = socket.gethostname()  # as both code is running on same pc
port = 5000
client_socket = None


def init_client():
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


def query_dolly(prompt):
    client_socket.send(prompt.encode())
    data = client_socket.recv(1024).decode()  # receive response

    return data

def client_program():
    
    init_client()
    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        data = query_dolly(message)  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
