import socket
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

def receive(connection):
    while True:
        try:
            msg = connection.recv(1024).decode(FORMAT)
            print(msg)
        except:
            print("An error occurred!")
            connection.close()
            break

def start():
    connection = connect()
    receive_thread = threading.Thread(target=receive, args=(connection,))
    receive_thread.start()
    
    print("Listening for messages. Press Ctrl+C to exit.")
    receive_thread.join()

if __name__ == "__main__":
    start()
