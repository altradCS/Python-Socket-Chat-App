import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
PRIVATE_PREFIX = "/msg"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    # Prompt the client for a username
    # conn.send("Enter your username: ".encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)

    with clients_lock:
        clients[username] = conn  # Store the client by username

    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg.startswith(PRIVATE_PREFIX):
                handle_private_message(username, msg)
            else:
                print(f"[{username}] {msg}")
                broadcast_message(f"[{username}] {msg}", conn)

    finally:
        with clients_lock:
            del clients[username]
            conn.close()
            print(f"[DISCONNECTED] {username} Disconnected")

def broadcast_message(msg, sender_conn):
    """Send a message to all clients except the sender."""
    with clients_lock:
        for conn in clients.values():
            if conn != sender_conn:
                conn.sendall(msg.encode(FORMAT))

def handle_private_message(sender_username, msg):
    """Handle private messaging between clients."""
    try:
        parts = msg.split(" ", 2)  # Split the message into command, recipient, and content
        recipient_username = parts[1]  # Directly get the recipient's username
        message_content = parts[2]

        with clients_lock:
            if recipient_username in clients:
                recipient_conn = clients[recipient_username]
                recipient_conn.sendall(f"Private from [{sender_username}]: {message_content}".encode(FORMAT))
            else:
                sender_conn = clients[sender_username]
                sender_conn.sendall(f"User {recipient_username} not found!".encode(FORMAT))
    except Exception as e:
        sender_conn = clients[sender_username]
        sender_conn.sendall(f"Error sending private message: {str(e)}".encode(FORMAT))

def send_broadcast_message():
    """Allow server to send broadcast messages."""
    while True:
        msg = input("[SERVER] Broadcast message: ")
        broadcast_message(f"[SERVER: {msg}", None)  # Broadcast from server

def start():
    print('[SERVER STARTED]!')

    broadcast_thread = threading.Thread(target=send_broadcast_message)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
