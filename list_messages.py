import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

def connect():
    """Establish connection to the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def start():
    """Receive and print messages from the server."""
    connection = connect()
    print("Connected. Listening for messages...")

    try:
        while True:
            msg = connection.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        connection.close()
        print("Connection closed.")


start()
