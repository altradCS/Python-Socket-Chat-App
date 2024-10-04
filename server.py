import threading
import socket
import threading
from tkinter import messagebox
import smtplib 
import time

PORT = 8080
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
clients_lock = threading.Lock()
disconnected_clients = {}


def handle_client(conn, addr):
    
    info_input = conn.recv(1024).decode(FORMAT)
    info_split = info_input.split(",")
    clients_info={"username":info_split[0],"email":info_split[1], "ms_to_receive":[]}
    

    with clients_lock:
        clients[conn] = clients_info  # Store the connection and username
    print(f"A wild {clients[conn]["username"]} appear.")

    for c in list(disconnected_clients): 
        if clients_info["email"] == disconnected_clients[c]["email"]: 
            for ms in disconnected_clients[c]["ms_to_receive"]:  
                conn.sendall(ms.encode(FORMAT))
                time.sleep(0.5)
            disconnected_clients.pop(c)
            break 

    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if not msg:
            break

        if msg == DISCONNECT_MESSAGE:
            disconnected_clients[conn]=clients[conn]
            clients.pop(conn)
            connected = False
            continue  # skip sending the disconnect message
        # Process direct messages
        process_message(conn, msg)

    # finally:
    #     with clients_lock:
    #         del clients[conn]

    #     conn.close()


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
            if username["username"] == recipient:  # Match the recipient by username
                conn.sendall(f"[DM from {clients[sender_conn]["username"]}]: {message}".encode(FORMAT))
                return
    # If recipient not found, send an error message to the sender
    for conn, username in disconnected_clients.items():
        if username["username"] == recipient:
            try:
                sender_conn.sendall(f"User '{recipient}' is offline. an email have been sent to alert them".encode(FORMAT))
                sender = "connectedzwebapp@gmail.com"
                receiver = username["email"]
                password = "hnef ovew lgja twqv"
                subject = f"{clients[sender_conn]['username'].capitalize()} via ConnectedZ"
                body = f"{clients[sender_conn]['username'].capitalize()} sent you a direct message!\nPlease connect to the server to view the message."
                email_message = f"Subject: {subject}\n\n{body}"

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, receiver, email_message)
                username["ms_to_receive"].append(f"[DM from {clients[sender_conn]["username"]}]: {message}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


            return
    sender_conn.sendall(f"[ERROR] User '{recipient}' not found.".encode(FORMAT))


def broadcast_message(message, sender_conn):
    """Send a message to all clients except the sender."""
    with clients_lock:
        
        for c in clients:
            if c != sender_conn:  # Do not send the message back to the sender
                c.sendall(f"Broadcast from {clients[sender_conn]["username"]}: {message}".encode(FORMAT))
        for c in disconnected_clients:
            if c != sender_conn:
                try:
                    sender = "connectedzwebapp@gmail.com"
                    receiver = disconnected_clients[c]["email"]
                    password = "hnef ovew lgja twqv"
                    subject = f"{clients[sender_conn]['username'].capitalize()} via ConnectedZ"
                    body = f"{clients[sender_conn]['username'].capitalize()} broadcast you a message!\nPlease connect to the server to view the message."
                    email_message = f"Subject: {subject}\n\n{body}"

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender, password)
                    server.sendmail(sender, receiver, email_message)
                    disconnected_clients[c]["ms_to_receive"].append(f"Broadcast from {clients[sender_conn]["username"]}: {message}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
                
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

def stop(closing):
    global stop_server
    stop_server = True
    if not closing:
        messagebox.showinfo("Server Stopped", "The server has been stopped.")
    server.close()  # Close the server when stopping

