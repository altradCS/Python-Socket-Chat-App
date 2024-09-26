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


def broadcast(message, sender_conn=None):
    """
    Send a message to all connected clients except the sender (if applicable).
    """
    with clients_lock:
        for client_conn, client_id in clients.items():
            if client_conn != sender_conn:  # Don't send to the sender
                try:
                    client_conn.sendall(message)
                except Exception as e:
                    print(f"[ERROR] Failed to send message to {client_id}: {e}")
                    clients.pop(client_conn)


def handle_client(conn, addr):
    with clients_lock:
        clients[conn] = f"{addr}"

    print(f"[NEW CONNECTION] {addr} connected")

    try:
        connected = True
        while connected:
            try:
                msg = conn.recv(1024).decode(FORMAT)
                if not msg:
                    break

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                # Log the message received by the server
                print(f"[{addr}] Received: {msg}")

                # Ensure the message starts with '@'
                if msg.startswith("@"):
                    # Check if message has at least two parts (e.g., @client_id: message)
                    if ":" in msg:
                        target_client, message = msg[1:].split(":", 1)  # Only split once

                        # Handling @all case
                        if target_client.strip().lower() == "all":
                            # Log the broadcast message
                            print(f"[{addr}] Broadcasting to all clients: {message}")

                            # Broadcast message to all clients
                            broadcast(f"[{clients[conn]}] {message}".encode(FORMAT), sender_conn=conn)
                        else:
                            # Send to specific client
                            found = False
                            with clients_lock:
                                for client_conn, client_id in clients.items():
                                    if target_client.strip() in client_id:  # matching target client
                                        print(f"[{addr}] Sending to {client_id}: {message}")
                                        client_conn.sendall(
                                            f"[{clients[conn]} -> {client_id}] {message}".encode(FORMAT))
                                        found = True
                                        break
                            if not found:
                                conn.sendall(f"[SERVER] Client {target_client} not found.".encode(FORMAT))
                    else:
                        # Invalid format (missing ':')
                        conn.sendall(
                            f"[SERVER] Invalid format. Use '@client_id: message' or '@all: message'.".encode(FORMAT))
                else:
                    # Handle messages that don't follow the '@client_id: message' or '@all: message' format
                    conn.sendall(
                        f"[SERVER] Invalid message format. Use '@client_id: message' or '@all: message'.".encode(
                            FORMAT))

            except ConnectionResetError:
                print(f"[ERROR] Connection with {addr} was reset.")
                break

    except Exception as e:
        print(f"[ERROR] Exception in handling client {addr}: {e}")
    finally:
        with clients_lock:
            clients.pop(conn, None)
        conn.close()
        print(f"[DISCONNECT] {addr} Disconnected")


def server_console():
    """
    Allows server to send messages to all clients.
    Type your message in the server terminal to broadcast it to all clients.
    """
    while True:
        msg = input()
        if msg == 'q':
            break
        broadcast(f"[SERVER] {msg}".encode(FORMAT))


def start():
    print('[SERVER STARTED]! Listening for connections...')
    server.listen()

    # Start server console for broadcasting messages
    console_thread = threading.Thread(target=server_console, daemon=True)
    console_thread.start()

    while True:
        try:
            conn, addr = server.accept()
            with clients_lock:
                clients[conn] = f"{addr}"
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except Exception as e:
            print(f"[ERROR] Exception in accepting connections: {e}")


if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        print(f"[ERROR] Server encountered an error: {e}")
    finally:
        server.close()
