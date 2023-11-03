import socket
from hashlib import sha256
import pickle
def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.100.103"
    server_port = 5555
    connection = True
    client.connect((server_ip, server_port))
    message = login_try()
    client.send(message)

    log_auth = client.recv(1024)
    log_auth = log_auth.decode("utf-8")

    if log_auth != "True": connection == False

    while connection:

        message = input("Type your message: ")
        client.send(message.encode("utf-8"))
        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            print("Closed message received.")
            break

        print(f"Received a message: {response}")

    client.close()
    print("Connection to server as been closed.")

def login_try():
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    hash_pass = sha256((username + password).encode("utf-8")).hexdigest()
    hash_check = sha256((hash_pass + username).encode("utf-8")).hexdigest()
    return pickle.dumps([username, hash_check])

run_client()
