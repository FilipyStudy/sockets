#Filipy da Silva Furtado
#Programa para CRUD em bancos de dados MySQL
import socket
import threading
import mysql.connector
import pickle

connector = mysql.connector.connect(
    host="localhost",
    password="password",
    user="root"
)
cursor = connector.cursor()

def login_verify(arr):
    try:
        cursor.execute(f"SELECT * FROM python_sockets.login WHERE username = '{arr[0].decode('utf-8')}'"
                       f" AND hash_check = '{arr[1].decode('utf-8')}'")
        return True
    except Exception as e:
        return f"Error: {e}"

def run_server():
    server_ip = "192.168.100.103"
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
        request = client_sock.recv(1024)
        request = pickle.loads(request)
        if(login_verify(request)):
                client_sock.send("True".encode("utf-8"))
                print(f"Accepted connection with: {client_addr[0]}:{client_addr[1]}")
        else:
            client_sock.send("Login error".encode("utf-8"))
            client_sock.close()
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

run_server()
