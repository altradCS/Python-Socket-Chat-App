import socket
import threading
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = {}
clients_lock = threading.Lock()

def create_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            server.bind(ADDR)
            return server
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Port {PORT} is busy. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise
    
    raise Exception(f"Could not bind to port {PORT} after {max_attempts} attempts")

def broadcast(message, sender_addr):
    with clients_lock:
        for client_addr, client_socket in clients.items():
            if client_addr != sender_addr:
                try:
                    client_socket.send(message.encode(FORMAT))
                except:
                    print(f"Error broadcasting to {client_addr}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg.startswith("@"):
                parts = msg.split(" ", 1)
                if len(parts) == 2:
                    recipient, message = parts
                    recipient_addr = tuple(recipient[1:].split(':'))
                    recipient_addr = (recipient_addr[0], int(recipient_addr[1]))
                    if recipient_addr in clients:
                        clients[recipient_addr].send(f"[Private from {addr}] {message}".encode(FORMAT))
                    else: conn.send(f"User {recipient_addr} not found".encode(FORMAT))
                else:
                    conn.send("Invalid private message format".encode(FORMAT))
            else:
                print(f"[{addr}] {msg}")
                broadcast(f"[{addr}] {msg}", addr)
    finally:
        with clients_lock:
            del clients[addr]
        conn.close()
        print(f"[DISCONNECTION] {addr} Disconnected")

def start(server):
    print('[SERVER STARTED]!')
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients[addr] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def server_input():
    while True:
        message = input("Server message: ")
        if message.lower() == 'q':
            break
        broadcast(f"[SERVER] {message}", None)

if __name__ == "__main__":
    try:
        server = create_server_socket()
        server_thread = threading.Thread(target=start, args=(server,))
        server_thread.start()
        
        input_thread = threading.Thread(target=server_input)
        input_thread.start()
        
        server_thread.join()
        input_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Server shutting down.")
