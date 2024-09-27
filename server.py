import socket
import time
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = {}
clients_lock = threading.Lock()

def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            server_socket.bind(ADDR)
            return server_socket
        except OSError as error:
            if error.errno == 98:  # Port is already in use
                print(f"Port {PORT} is in use. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise
    
    raise Exception(f"Unable to bind to port {PORT} after {max_attempts} attempts")

def broadcast(message, sender_address):
    with clients_lock:
        for client_address, client_socket in clients.items():
            if client_address != sender_address:
                try:
                    client_socket.send(message.encode(FORMAT))
                except:
                    print(f"Failed to send message to {client_address}")

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        connected = True
        while connected:
            msg = client_socket.recv(1024).decode(FORMAT)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg.startswith("@"):
                parts = msg.split(" ", 1)
                if len(parts) == 2:
                    recipient, message = parts
                    recipient_address = tuple(recipient[1:].split(':'))
                    recipient_address = (recipient_address[0], int(recipient_address[1]))
                    if recipient_address in clients:
                        clients[recipient_address].send(f"[Private from {client_address}] {message}".encode(FORMAT))
                    else:
                        client_socket.send(f"User {recipient_address} not found".encode(FORMAT))
                else:
                    client_socket.send("Invalid private message format".encode(FORMAT))
            else:
                print(f"[{client_address}] {msg}")
                broadcast(f"[{client_address}] {msg}", client_address)
    finally:
        with clients_lock:
            del clients[client_address]
        client_socket.close()
        print(f"[DISCONNECTION] {client_address} disconnected.")

def start_server(server_socket):
    print('[SERVER STARTED]')
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        with clients_lock:
            clients[addr] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def admin_input():
    while True:
        admin_message = input("Server message: ")
        if admin_message.lower() == 'q':
            break
        broadcast(f"[SERVER] {admin_message}", None)

if __name__ == "__main__":
    try:
        server_socket = create_server_socket()
        server_thread = threading.Thread(target=start_server, args=(server_socket,))
        server_thread.start()
        
        admin_thread = threading.Thread(target=admin_input)
        admin_thread.start()
        
        server_thread.join()
        admin_thread.join()
    except Exception as error:
        print(f"Error occurred: {error}")
    finally:
        print("Server is shutting down.")
