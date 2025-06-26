# Filipy da Silva Furtado
# Programa para CRUD em bancos de dados MySQL
# Script para execução do servidor.

#Faz importação das libs inerentes ao funcionamento do script.
import socket
import threading
import mysql.connector
import pickle
from datetime import datetime

#Cria objeto para conexão e realização de CRUDS no script.
connector = mysql.connector.connect(
    host="localhost",
    password="password",
    user="root"
)

#Cria objeto para manuseio do CRUD.
cursor = connector.cursor()


#Realiza verificação dos dados enviados pela função login_try do script cliente.
#Função realiza consulta no banco de dados.
#Retorna verdadeiro se os dados enviados pelo cliente estão na tabela.
def login_verify(arr):
    try:
        cursor.execute(f"SELECT * FROM python_sockets.login WHERE username = '{arr[0].decode('utf-8')}'"
                       f" AND hash_check = '{arr[1].decode('utf-8')}'")

        if cursor != 0: return False
        else: return True

    except Exception as e:
        return f"Error: {e}"


#Define funcionamento principal do servidor.
#Recebe e cria novas threads para conexão.
def run_server():
    server_ip = "endereço do host com servidor (rede LAN)"
    server_port = 5555 #Porta usada pelo servidor.

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

#faz o a verificação de login para entrar no servidor e cria uma nova conexão com o cliente.

def handle_client(client_sock, client_addr):
    try:
        request = client_sock.recv(1024) #Define o tamanho máximo de dados a ser recebido.
        request = pickle.loads(request) #
        if login_verify(request):
            client_sock.send("True".encode("utf-8"))
            print(f"Accepted connection with: {client_addr[0]}:{client_addr[1]}")
            localtime = f"{datetime.hour}{datetime.minute}{datetime.yaer}{datetime.month}{datetime.day}"
            while True:
                request = client_sock.recv(1024)
                request = request.decode("utf-8")
                if request.lower() == "close":
                    client_sock.send("The server closed your connection!".encode("utf-8"))
                    break
                print(f"Received: {request}")
                client_sock.send("Received".encode("utf-8"))
        else:
            client_sock.send("Login error, closing the connection".encode("utf-8"))
            client_sock.close()

    except Exception as e:
        print(f"An error occurs on handle_client: {e}")
    finally:
        client_sock.close()
        print(f"Connection to client {client_addr[0]}:{client_addr[1]} closed.")


#Executa o servidor.
if __name__ == "__main__": run_server()
