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
    message = msg.encode(FORMAT)
    client.send(message)

def receive(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            print(msg)
        except:
            print("An error occurred!")
            client.close()
            break

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    receive_thread = threading.Thread(target=receive, args=(connection,))
    receive_thread.start()

    while True:
        msg = input()
        if msg.lower() == 'q':
            break
        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')
    connection.close()

if __name__ == "__main__":
    start()
