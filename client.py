import threading
import socket
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        print(f"Connected to the server at {ADDR}")
        return client
    
    except Exception as e:
        print(f"Unable to connect to server: {e}")
        return None


def send(client, msg):
    try:
        message = msg.encode(FORMAT)
        client.send(message)
        
    except Exception as e:
        print(f"Unable to send message: {e}")

def receive(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if not msg:
                print("Server connection ended.")
                break
            print(msg)  
            
        except Exception as e:
            print(f"Connection error: {e}")
            break

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    if not connection:
        print("Failed to connect. Exiting.")
        return
    
    # Enter username to be sent to the server
    username = input("Enter your username: ")
    send(connection, username)
    
    # Start a thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive, args=(connection,))
    receive_thread.start()
    
    print("Message (q for quit): ")
    while True:
        msg = input("")

        if msg == 'q':
            send(connection, DISCONNECT_MESSAGE)
            break

        send(connection, msg)

    time.sleep(1)
    connection.close()
    print('Disconnected')


start()
