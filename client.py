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

def receive(client):
    while True:
        try:
            # Receiving messages from the server
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(f"\n{msg}")
                print("Message (q for quit): ", end='', flush=True)
            else:
                break  
        except:
            print("Error receiving data.")
            break

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect() 
    receive_thread = threading.Thread(target=receive, args=(connection,))  
    receive_thread.start()

    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            break

        send(connection, msg)  

    send(connection, DISCONNECT_MESSAGE)  
    time.sleep(1)
    print('Disconnected')


start()
