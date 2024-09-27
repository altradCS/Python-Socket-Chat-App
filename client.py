import socket
import threading
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    """Send a message to the server."""
    message = msg.encode(FORMAT)
    client.send(message)

def receive(client):
    """Receive messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message:
                print(message)
        except:
            print("Error receiving message.")
            break

def start():
    """Start the client to send and receive messages."""
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return 

    connection = connect()

    # Start a thread to handle receiving messages
    receive_thread = threading.Thread(target=receive, args=(connection,))
    receive_thread.start()

    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            send(connection, DISCONNECT_MESSAGE)
            time.sleep(1)
            break

        send(connection, msg)

    print('Disconnected')


start()
