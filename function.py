import socket
import customtkinter as ctk
from client_origin import *
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import server

not_full_screen=False
server_stop_flag=False


class custom_frame(ctk.CTkFrame):
    def __init__(self,root,f_color, corner_radius, user_image, image_send, connection, start_time, btn):
        super().__init__(root.middle_frame, fg_color=f_color, corner_radius=corner_radius)
        self.connection = connection
        self.btn = btn
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=0)
        # Add content inside the newly created frame
        self.display_text = ctk.CTkScrollableFrame(self, width=700, height=400, corner_radius=10, fg_color="#171717")
        self.display_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.display_text.grid_columnconfigure(1, weight=1)
        # display_text.grid_propagate(False)
        
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1)
        
        entry = ctk.CTkEntry(control_frame, width=300, height=35)
        entry.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        send_to_server = ctk.CTkButton(control_frame, text="Send",image=image_send, compound=tk.LEFT,
                               font=("JetBrains Mono", 12),
                               command= lambda: display_send(self.connection, entry.get(), self.display_text, start_time, user_image),
                               width=40,)
        send_to_server.grid(row=0, column=2)
        
        disconnect_btn = ctk.CTkButton(control_frame, text="Send",image=image_send, compound=tk.LEFT,
                               font=("JetBrains Mono", 12),
                               command= lambda: (self.pack_forget(),self.btn.grid_forget(), send(self.connection, DISCONNECT_MESSAGE)),
                               width=40,)
        disconnect_btn.grid(row=0, column=3)
        
        




def get_img(img, width=20, height=20):
    start_img = Image.open(img)
    start_resize = start_img.resize((width, height))
    final = ImageTk.PhotoImage(start_resize)
    return final
def close_win(root):
    root.after(300, root.destroy())
def minimize_window(root, top_win):
    root.withdraw()
def onRootDeiconify(root): 
    root.deiconify()
def maximize_win(master,root):
    global not_full_screen
    if not_full_screen:
        root.geometry('825x530')
        not_full_screen = False
    else:
        root.geometry(f'{root.winfo_screenwidth()}x{
                      root.winfo_screenheight()}+0+0')
        not_full_screen = True
    
def create_new_frame(root,btn, frame_name, connection, user_image, image_send):
    start_time = time.time()
    apply_color(btn, root.side_frame)
    for a_frame in root.middle_frame.winfo_children():
        a_frame.pack_forget()
    if frame_name not in root.frame_dict:
        temp_frame=custom_frame(root, "#242424", 0, user_image, image_send, connection, start_time, btn)
        root.frame_dict[frame_name] = temp_frame
        threading.Thread(target=get_message, args=(temp_frame.display_text, temp_frame.connection,start_time,user_image)).start()
    else:
        root.frame_dict[frame_name].connection = connection
        root.frame_dict[frame_name].btn = btn
        
        threading.Thread(target=get_message, args=(root.frame_dict[frame_name].display_text, connection,start_time,user_image)).start()

    # Bring the frame to the front
    show_frame(root.frame_dict[frame_name])

def apply_color(btn, frame):
    for button in frame.winfo_children():
        button.configure(fg_color="#333333")
    btn.configure(fg_color="#114AAF")

def show_frame(frame):
    frame.pack(fill="both", expand=True)


def get_message(frame, connection, start_time, user_image):
    while True:
        try:
            # Receive data from the connection
            message = connection.recv(2048)
            
            if not message:
                # If no data is received, it means the connection is closed
                break

            decoded_message = message.decode("utf-8")
            row_position = int(time.time() - start_time)
            
            # Display the received message
            tk.Label(frame, image=user_image, text=" " + decoded_message, font=("JetBrains Mono", 15), 
                     compound=tk.RIGHT, bg="#171717", fg="white").grid(row=row_position, column=2, padx=10, sticky="e")
        except (ConnectionResetError, socket.error):
            # Silently handle connection reset or socket errors
            break
        except Exception:
            # Silently handle any other exceptions
            break
def display_send(connection, message, frame, start_time,user_image):
    row_positon = int(time.time()-start_time)
    send(connection, message)
    if message:
        tk.Label(frame, image=user_image, text=f"You: {message}", font=("JetBrains Mono",15), compound=tk.LEFT,bg="#171717", fg="white").grid(row=row_positon, column =0, padx=10, sticky="w")

def move(event, window):
    x = window.winfo_x()-window.startX + event.x
    y = window.winfo_y()-window.startY + event.y
    window.geometry(f'+{x}+{y}')

def origin_cords(event, window):
    window.startX = event.x
    window.startY = event.y
def start_stop_server(root):
    global server_stop_flag
    if root.server_status:

        server_starter = threading.Thread(target=server.start)
        server_starter.start()
        root.server_button.configure(image=root.stop_img,
                                           text="Stop Server",
                                           fg_color="red",
                                           hover_color="red",
                                           border_width=0,
                                           width=40,
                                           font=("JetBrains Mono", 12,"bold"),
                                           compound=tk.LEFT)
        root.server_status = False
    else:
        root.server_button.configure(      image=root.start_img,
                                           text="Start Server",
                                           fg_color="#333333",
                                           hover_color="#02733E",
                                           border_color="#02733E",
                                           border_width=2,
                                           width=40,
                                           font=("JetBrains Mono", 12,"bold"),
                                           compound=tk.LEFT)
        server.stop()
        root.server_status = True
