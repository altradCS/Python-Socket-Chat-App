import socket
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(ADDR)
    return client_socket

def receive_messages(connection_socket):
    while True:
        try:
            message = connection_socket.recv(1024).decode(FORMAT)
            print(message)
        except:
            print("An error occurred!")
            connection_socket.close()
            break

def start_client():
    connection_socket = connect_to_server()

    receive_thread = threading.Thread(target=receive_messages, args=(connection_socket,))
    receive_thread.start()
    
    print("Waiting for messages. Press Ctrl+C to quit.")
    
    receive_thread.join()

if __name__ == "__main__":
    start_client()
