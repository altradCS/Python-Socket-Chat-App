import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()

def broadcast(message, exclude_client=None):
    """Broadcast a message to all clients, optionally excluding one."""
    with clients_lock:
        for client, addr in clients.items():
            if client != exclude_client:  # Exclude sender if specified
                try:
                    client.sendall(message.encode(FORMAT))
                except:
                    # Handle if the client has disconnected
                    remove_client(client)

def remove_client(client):
    """Safely remove a client from the list of connected clients."""
    with clients_lock:
        if client in clients:
            del clients[client]

def handle_client(conn, addr):
    """Handle communication with a single client."""
    print(f"[NEW CONNECTION] {addr} connected.")
    with clients_lock:
        clients[conn] = addr  # Add client to the list

    try:
        while True:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] disconnected.")
                break

            print(f"[{addr}] {msg}")
            broadcast(f"[{addr}] {msg}", exclude_client=conn)
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        remove_client(conn)
        conn.close()

def send_from_server():
    """Allow the server to send messages to all clients."""
    while True:
        msg = input("Server Message: ")
        if msg:
            broadcast(f"[SERVER]: {msg}")

def start():
    """Start the server and handle clients."""
    print('[SERVER STARTED]! Listening for connections...')
    server.listen()

    # Thread to allow the server to send its own messages
    threading.Thread(target=send_from_server, daemon=True).start()

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SERVER SHUTTING DOWN]")
    finally:
        server.close()


    start()
