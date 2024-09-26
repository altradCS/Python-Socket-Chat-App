import socket
import threading
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def receive_messages(client):
    """
    Listen to messages from the server in a separate thread.
    """
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if not msg:
                break
            print(msg)
        except Exception as e:
            print(f"[ERROR] Failed to receive message: {e}")
            break


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        return client
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return None


def send(client, msg):
    """
    Send a message to the server.

    - To broadcast a message to all clients, use the format: '@all: your message'
    - To send a message to a specific client, use the format: '@client_id: your message'
      (where 'client_id' is the address of the client, such as '127.0.0.1:5051')
    """
    try:
        message = msg.encode(FORMAT)
        client.send(message)
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")


def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    if not connection:
        return

    # Start receiving messages in a separate thread
    threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()

    print("Instructions for sending messages:")
    print("- To broadcast to all clients: @all: message")
    print("- To send to a specific client: @client_id: message (e.g., @127.0.0.1:5051: Hello)")
    print("- Type 'q' to disconnect")

    while True:
        msg = input("Message (q for quit, @all: for broadcast): ")

        if msg == 'q':
            break

        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')


if __name__ == "__main__":
    start()
