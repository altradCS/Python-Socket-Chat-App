import socket
import time
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

def send_message(client_socket, message):
    encoded_msg = message.encode(FORMAT)
    client_socket.send(encoded_msg)

def receive_messages(client_socket):
    while True:
        try:
            received_msg = client_socket.recv(1024).decode(FORMAT)
            print(received_msg)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def start_client():
    user_input = input('Do you want to connect? (yes/no) ')
    if user_input.lower() != 'yes':
        return

    connection_socket = connect_to_server()

    receiver_thread = threading.Thread(target=receive_messages, args=(connection_socket,))
    receiver_thread.start()

    while True:
        message = input()
        if message.lower() == 'q':
            break
        send_message(connection_socket, message)

    send_message(connection_socket, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected from the server.')
    connection_socket.close()

if __name__ == "__main__":
    start_client()
