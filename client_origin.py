import socket
import time
import threading

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
    message = msg.encode(FORMAT)
    client.send(message)


def receive_messages(client):
    """Receive messages from the server."""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
        except Exception as e:
            print(f"[ERROR] {e}")
            break


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()

    # Start a thread to receive messages from the server
    thread = threading.Thread(target=receive_messages, args=(connection,))
    thread.start()

    while True:
        msg = input("Message (format: recipient:message or 'q' for quit): ")

        if msg == 'q':
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')
    connection.close()

