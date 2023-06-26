import  socket

from transformers import pipeline
import torch

def server_program():
    # get the hostname
    #host = socket.gethostname()
    host = "172.31.22.250"
    port = 80 # initiate port no above 1024
    print("host",host)

    instruct_pipeline = pipeline(model="databricks/dolly-v2-3b",
                                 torch_dtype=torch.bfloat16,
                                 trust_remote_code=True,
                                 device_map="auto")
    print("Start")


    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(10240).decode()
        if not data:
            # if data is not received break
            print("Void data received")
            break
        print("from connected user: " + str(data))
        income = str(data)
        res = instruct_pipeline(income)
        print(res[0]["generated_text"])
        data_out = res[0]["generated_text"].encode()
        conn.send(data_out)  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
