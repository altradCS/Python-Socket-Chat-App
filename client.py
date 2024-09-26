import socket
import time
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
PRIVATE_PREFIX = "/msg"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive_messages(client):
    """Function to receive messages from the server in a separate thread."""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)  # Print incoming messages
        except Exception as e:
            print("Error receiving message:", e)
            break

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    print(f"Connected to the server!")

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    receive_thread.daemon = True
    receive_thread.start()

    # Receive username input after connection
    username = input("Enter your username: ")
    send(connection, username)

    while True:
        msg = input("Message (q for quit, /msg <username> <message> for private): ")

        if msg == 'q':
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')

start()
