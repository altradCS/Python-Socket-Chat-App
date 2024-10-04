import threading
import socket
import threading
from tkinter import messagebox

PORT = 8080
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
        # Ask for a username
        username = conn.recv(1024).decode(FORMAT)
        with clients_lock:
            clients[conn] = username  # Store the connection and username
        print(f"[USERNAME SET] {username} from {addr}")

        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue  # skip sending the disconnect message

            # Process direct messages
            process_message(conn, msg)

    finally:
        with clients_lock:
            del clients[conn]

        conn.close()


def process_message(conn, msg):
    """Process and route messages to specific clients."""
    parts = msg.split(":", 1)  # Expecting format "recipient:message"
    if len(parts) == 2:
        recipient, message = parts
        send_to_specific_client(recipient.strip(), message.strip(), conn)
    else:
        broadcast_message(msg, conn)  # If no recipient, broadcast


def send_to_specific_client(recipient, message, sender_conn):
    """Send a message to a specific client."""
    with clients_lock:
        for conn, username in clients.items():
            if username == recipient:  # Match the recipient by username
                conn.sendall(f"[DM from {clients[sender_conn]}]: {message}".encode(FORMAT))
                return
    # If recipient not found, send an error message to the sender
    sender_conn.sendall(f"[ERROR] User '{recipient}' not found.".encode(FORMAT))


def broadcast_message(message, sender_conn):
    """Send a message to all clients except the sender."""
    with clients_lock:
        
        for c in clients:
            if c != sender_conn:  # Do not send the message back to the sender
                c.sendall(f"Broadcast from {clients[sender_conn]}: {message}".encode(FORMAT))
stop_server = False

def start():
    print('[SERVER STARTED]! Waiting for connections...')
    try:
        server.listen()
    except Exception:
        pass
    
    while not stop_server:
        try:
            # Use a short timeout to check the flag periodically
            server.settimeout(1)  # Check for new connections every 1 second
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except socket.timeout:
            # Timeout is expected, just continue to check the stop flag
            continue
        except Exception:
            pass

def stop():
    global stop_server
    stop_server = True
    messagebox.showinfo("Server Stopped", "The server has been stopped.")
    server.close()  # Close the server when stopping

