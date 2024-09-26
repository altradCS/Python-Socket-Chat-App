from colorama import Fore, Style, init
import threading
import socket
import time
import sys


PORT = 5050
HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()


def broadcast(message, sender = None):
    """Broadcasts a message to all connected clients except the sender."""
    with clients_lock:
        for client in list(clients):  # Create a list to avoid modifying the set during iteration
            if client != sender:
                try:
                    client.send(message)
                    print(clients)
                except Exception as e:
                    print(f"[ERROR] Could not send message to {client}: {e}")
                    clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    
    try:

        # The first message received from the client should be the username
        username = conn.recv(HEADER).decode(FORMAT)
        print(f"[NEW USER] {username} connected.")  

        # Announce the new client connection to all clients
        join_message = f"{Fore.GREEN}{username} has joined the chat.{Style.RESET_ALL}".encode(FORMAT)
        broadcast(join_message, conn)  # Announce to all clients except the new one
        
        connected = True
        while connected:
            msg = conn.recv(HEADER).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                break

            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            formatted_msg = f"{msg}".encode(FORMAT)
            broadcast(formatted_msg, conn)  # Broadcast the message, excluding the sender
            sys.stdout.write("\033[K")
            print(f"\r[{timestamp}] {msg}")
            
            sys.stdout.write("Server: ")
            sys.stdout.flush()
            
    finally:
        with clients_lock:
            clients.remove(conn)
            
        leave_message = f"{Fore.RED}{username} has left the chat.{Style.RESET_ALL}".encode(FORMAT)
        broadcast(leave_message)  # Announce to all clients that the user has left
        
        conn.close()
        sys.stdout.write("\033[K")
        print(f"[Connection Closed] {username} disconnected.")
        sys.stdout.write("Server: ")
        sys.stdout.flush()

def server_broadcast_input():
    """Handles server-side input to send messages to all connected clients."""
    while True:
        sys.stdout.write("Server: ")
        sys.stdout.flush()
        msg = input("")

        if msg:
            formatted_msg = f"{Fore.YELLOW}[SERVER]: {msg}{Style.RESET_ALL}".encode(FORMAT)
    
            broadcast(formatted_msg)  # Send to all clients
            print(f"[SERVER]: {msg}")

def start():
    init()
        
    print(f"[LISTENING] Server is listening on {SERVER}")
    server.listen()
    
    # Start a thread to handle server input for broadcasting
    input_thread = threading.Thread(target=server_broadcast_input, daemon=True)
    input_thread.start()
    
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)   
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")

print("[STARTING] Server is starting ...")
start()
