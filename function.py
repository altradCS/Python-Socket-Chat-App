import socket
import customtkinter as ctk
from client_origin import *
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

not_full_screen=True
global client_to_sever


def get_img(img, width=20, height=20):
    start_img = Image.open(img)
    start_resize = start_img.resize((width, height))
    final = ImageTk.PhotoImage(start_resize)
    return final
def close_win(root):
    root.after(300, root.destroy())
def minimize_window(root):
    pass
def maximize_win(master,root):
    global not_full_screen
    if not_full_screen:
        root.geometry('900x450')
        not_full_screen = False
    else:
        root.geometry(f'{root.winfo_screenwidth()}x{
                      root.winfo_screenheight()}+0+0')
        not_full_screen = True
    
def create_new_frame(root,btn, frame_name, connection, user_image, image_send):
    start_time = time.time()
    apply_color(btn, root.side_frame)
    # Only create the frame if it doesn't already exist
    if frame_name not in root.frame_dict:
        temp_frame = ctk.CTkFrame(root.middle_frame, fg_color="#242424", corner_radius=0)
        temp_frame.grid(row=0, column=0,padx=27, pady=2)
        root.frame_dict[frame_name] = temp_frame

        # Add content inside the newly created frame
        display_text = ctk.CTkScrollableFrame(temp_frame, width=700, height=400, corner_radius=10, fg_color="#171717")
        display_text.pack(pady=10)
        display_text.grid_columnconfigure(1, weight=1)
        # display_text.grid_propagate(False)
        
        control_frame = ctk.CTkFrame(temp_frame)
        control_frame.pack()
        
        entry = ctk.CTkEntry(control_frame, width=300, height=35)
        entry.grid(row=0, column=0)
        
        send_to_server = ctk.CTkButton(control_frame, text="Send",image=image_send, compound=tk.LEFT,
                               font=("JetBrains Mono", 12),
                               command= lambda: display_send(connection, entry.get(), display_text, start_time, user_image),
                               height=30)
        send_to_server.grid(row=0, column=1)
        
        threading.Thread(target=get_message, args=(display_text, connection,start_time,user_image)).start()
        

    # Bring the frame to the front
    show_frame(root.frame_dict[frame_name])

def apply_color(btn, frame):
    for button in frame.winfo_children():
        button.configure(fg_color="#333333")
    btn.configure(fg_color="#114AAF")

def show_frame(frame):
    frame.tkraise()


def get_message(frame, connection, start_time,user_image):

    while True:
        row_positon = int(time.time()-start_time)
        tk.Label(frame, image=user_image, text=" "+connection.recv(2048).decode("utf-8"), font=("JetBrains Mono",15), compound=tk.RIGHT, bg="#171717", fg="white" ).grid(row=row_positon, column =2, padx=10, sticky="e")
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