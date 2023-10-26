#Filipy da Silva Furtado
#Programa para CRUD em bancos de dados MySQL

import socket
import threading
import mysql.connector
from hashlib import sha256

def login_try():
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    hash_pass = sha256((username + password).encode("utf-8")).hexdigest()
    hash_check = sha256((hash_pass + username).encode("utf-8")).hexdigest()
    return hash_check
connector = mysql.connector.connect(
    host="localhost",
    password="password",
    user="root"
)
cursor = connector.cursor()

login = 'admin'
psw = 'password_hash'
hash_check = 'hash_check (password_hash + username)'
def login_verify():
    try:
        cursor.execute(f"SELECT * FROM python_sockets.login WHERE username = '{login}'"
                       f" AND psw = '{psw}'"
                       f" AND hash_check = '{hash_check}'")
        print("Sucesfull")
    except Exception as e:
        print(f"Erro: {e}")

def run_server():
    server_ip = "192.168.100.19"
    server_port = 5555

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, server_port))
        server.listen()

        while True:
            client_sock, client_addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_sock, client_addr))
            thread.start()

    except Exception as e:
        print(f"Error occurs: {e}")
    finally:
        server.close()
def handle_client(client_sock, client_addr):
    try:
        print(f"Accepted connection with: {client_addr[0]}:{client_addr[1]}")
        while True:
            request = client_sock.recv(1024)
            request = request.decode("utf-8")
            if request.lower() == "close":
                client_sock.send("The server closed your connection!".encode("utf-8"))
                break
            print(f"Received: {request}")
            client_sock.send("Received".encode("utf-8"))

    except Exception as e:
        print(f"An error occurs on handle_client: {e}")
    finally:
        client_sock.close()
        print(f"Connection to client {client_addr[0]}:{client_addr[1]} closed.")

