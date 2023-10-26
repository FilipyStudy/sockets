import socket


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.100.19"
    server_port = 5555

    client.connect((server_ip, server_port))

    while True:
        message = input("Enter your message: ")
        client.send(message.encode("utf-8"))

        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            print("Closed message received.")
            break

        print(f"Received a message: {response}")

    client.close()
    print("Connection to server as been closed.")


run_client()
