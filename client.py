import socket
import threading
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    """Connect to the server."""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        return client
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        return None

def send(client):
    """Send messages to the server."""
    while True:
        try:
            msg = input()
            if msg.lower() == 'q':
                break
            client.send(msg.encode(FORMAT))
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    
    try:
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        print('Disconnected')
    except Exception as e:
        print(f"Error during disconnect: {e}")
    finally:
        client.close()

def receive(client):
    """Receive messages from the server."""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def start():
    """Start the client and manage sending and receiving messages."""
    connection = connect()
    if connection is None:
        return  # Exit if the connection failed
    
    # Start a thread to listen for incoming messages
    threading.Thread(target=receive, args=(connection,), daemon=True).start()

    print("Type your messages below (type 'q' to quit):")
    send(connection)

start()
