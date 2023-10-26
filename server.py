import socket
import threading


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


run_server()
