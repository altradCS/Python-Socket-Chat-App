import threading
import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")

    try:
         # Receive the initial username
        username = conn.recv(1024).decode(FORMAT)
        if not username:
            return

        # Add the client to the list with the username as key
        with clients_lock:
            clients[username] = conn
        print(f"{addr}'s username is set to {username}")
        
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{get_timestamp()}] [{username}]: {msg}")
            
            # Check if message is a private message (starts with @username)
            if msg.startswith("@"):
                # Split the message into target username and actual message
                target_name, private_msg = msg.split(" ", 1)
                target_name = target_name[1:]  # Remove the "@" symbol
                
                with clients_lock:
                    target_conn = clients.get(target_name)

                if target_conn:
                    try:
                        target_conn.sendall(f"\n[DM] [{get_timestamp()}] [{username}]: {private_msg}".encode(FORMAT))
                    except:
                        print(f"Failed to send message to {target_name}")
                else:
                    conn.sendall(f"User {target_name} not found.".encode(FORMAT))
            else:
                with clients_lock:
                    for user, client_conn in clients.items():
                        if client_conn != conn:
                            client_conn.sendall(f"[{get_timestamp()}] [{username}]: {msg}".encode(FORMAT))
    
    except Exception as e:
        print(f"[ERROR] Exception occurred with {addr}: {e}")
        
    finally:
        with clients_lock:
            if username in clients and clients[username] == conn:
                del clients[username]

        conn.close()
        print(f"[DISCONNECTED] {addr} Disconnected")


def start():
    print('[SERVER STARTED]!')
    server.listen()
    
    while True:
        conn, addr = server.accept()
        
        # with clients_lock:
        #     clients.add(conn)
            
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        # Display the number of active connections
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


start()
