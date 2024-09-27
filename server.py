import threading
import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket and listen for connections
try:
    server.bind(ADDR)
    server.listen()
    print(f"[SERVER STARTED]! Listening for connections on {SERVER}:{PORT}...")
except Exception as e:
    print(f"Error starting server: {e}")
    exit()

clients = {}
clients_lock = threading.Lock()

def get_current_time():
    """Return the current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def broadcast(message):
    """Broadcast a message to all connected clients."""
    with clients_lock:
        for client in clients.keys():
            try:
                client.sendall(message.encode(FORMAT))
            except Exception as e:
                print(f"Error sending message to a client: {e}")

def handle_client(conn, addr):
    """Handle communication with a connected client."""
    print(f"[NEW CONNECTION] {addr} Connected")
    
    with clients_lock:
        clients[conn] = addr

    try:
        connected = True
        while connected:
            try:
                msg = conn.recv(1024).decode(FORMAT)
                if not msg:
                    break

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    continue
                
                # Add timestamp to the message and broadcast
                timestamped_message = f"[{get_current_time()}] [{addr}] {msg}"
                print(timestamped_message)
                broadcast(timestamped_message)

            except ConnectionResetError:
                print(f"Connection reset by {addr}.")
                break

    finally:
        with clients_lock:
            del clients[conn]
        
        conn.close()
        print(f"[DISCONNECTED] {addr} Disconnected")

def start():
    """Start the server and listen for incoming connections."""
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f"Error accepting a connection: {e}")

def broadcast_from_console():
    """Allow the server to take input from the console and broadcast it to all clients."""
    while True:
        try:
            message = input("Enter a message to broadcast (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Server shutting down.")
                break
            timestamped_message = f"[{get_current_time()}] [SERVER] {message}"
            broadcast(timestamped_message)
        except Exception as e:
            print(f"Error during console input: {e}")

# Start the broadcast console input thread
threading.Thread(target=broadcast_from_console, daemon=True).start()
start()
