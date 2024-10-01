import customtkinter as ctk
from function import *
import tkinter as tk
from tkinter import ttk
from client_origin import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
# from client_origin import *
class client_ui():
    def __init__(self,root):
        global close_img, maximize, minimize, menu_img, add,client_device,user_image, image_send
        self.number_of_client=0
        self.frame_dict = {}
        self.buttons = {}

        
        menu_img = get_img("assets\icon_app.png", 40,40)
        add =ctk.CTkImage(Image.open("assets\icons8-plus-50.png"),size=(30,30))
        client_device = ctk.CTkImage(Image.open("assets/icons8-cloud-computing-50.png"), size=(30,30))#get_img("assets/icons8-cloud-computing-50.png", 35,35)
        user_image = get_img("assets/icons8-user-48.png", 35, 35)
        image_send = get_img("assets/icons8-send-50.png",35,35)

        self.root = root
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.title("Client")
        self.root.overrideredirect(True)
        self.root.geometry("825x530")
        #title frame
        self.top_bar = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=0, height=50)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_bar.grid_columnconfigure(1, weight=1)
        #add side frame
        self.side_frame = ctk.CTkFrame(self.root, corner_radius=0,fg_color="#333333")
        self.side_frame.grid(row=1, column=0, sticky="nsew")
        #add middle frame
        self.middle_frame = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=0)
        self.middle_frame.grid(row=1, column=1, sticky="nsew")
        self.menu = tk.Button(self.top_bar,
                                image= menu_img,
                                bg="#333333",
                                activebackground="#114AAF",
                                relief='flat',
                                border=0,
                                font=("Roboto mono", 12, "bold"),
                                fg="white",
                                compound=tk.LEFT,
                                command=lambda: close_win(root),
                                width=56,
                                )
        self.menu.grid(row=0, column=0)
        self.add_connection = ctk.CTkButton(self.side_frame,
                                         text="",
                                         fg_color="#333333",
                                         hover_color="#114AAF",
                                         width=40,
                                         image=add,
                                         compound=tk.LEFT,
                                command=self.add_client_device
                                )
        self.add_connection.grid(row=10, column=0)
        
        self.title_frame = ctk.CTkFrame(self.top_bar,fg_color="#333333")
        self.title_frame.grid(row=0, column=2)


        # get icons for control frame
        close_img = get_img("assets/x.png", 30,30)
        maximize = get_img('assets/maximize-2_white.png',30,30)
        minimize = get_img("assets/minus_white.png",30,30)
        self.close = tk.Button(self.title_frame, text='',
                               image= close_img,
                               bg="#242424",
                               activebackground="#333333",
                            
                            relief='flat',
                            border=0,
                            width=30,
                            command=lambda: close_win(root))
        self.close.grid(row=0, column=2)
        self.minimize = tk.Button(self.title_frame, text='',
                                  image=minimize,
                                  bg="#242424",
                                  activebackground="#333333",
                               relief='flat',
                               border=0, width=30,
                               command=lambda: minimize_window(root))
        self.minimize.grid(row=0, column=0)
        self.maximize = tk.Button(self.title_frame, text='',
                                  image= maximize,
                                  bg="#242424",
                                  activebackground="#333333",
                               relief='flat',
                               border=0, width=30,
                               command=lambda: maximize_win(self,root))
        self.maximize.grid(row=0, column=1)
        self.prompt_label = ctk.CTkLabel(self.middle_frame, text="Press + to connect to the server", font=("JetBrains Mono",15, "italic"))
        self.prompt_label.pack(fill="none", expand=True)
    def add_client_device(self):
        self.prompt_label.destroy()
    
        connection = connect()
        name = self.get_name()
        connection.send(name.encode(FORMAT))

        self.buttons[name]=ctk.CTkButton(self.side_frame,
                                         text="",
                                         fg_color="#333333",
                                         hover_color="#114AAF",
                                         width=40,
                                         image=client_device,
                                         compound=tk.LEFT,
                                         
                                         )
        self.buttons[name].configure(command=lambda frame=self.number_of_client, name = self.buttons[name]: create_new_frame(self,name, f"frame {frame}",connection, user_image, image_send))
        # create_button(self.buttons[name])
        self.buttons[name].grid(row=self.number_of_client+1,column=0)
        self.number_of_client += 1
    def get_name(self):
        names = [
        "Alice",
        "Bob",
        "Charlie",
        "David",
        "Eve",
        "Frank",
        "Grace",
        "Heidi",
        "Ivan",
        "Judy"
        ]
        while True:
            choose=random.choice(names)
            if messagebox.askyesno("Name Suggestion", f"Do you want to be call as {choose}?"):
                names.remove(choose)
                return choose

        

            




window = ctk.CTk()

Ui =client_ui(window)
Ui.top_bar.bind('<Button-1>', lambda e: origin_cords(e, window))
Ui.top_bar.bind('<B1-Motion>', lambda e: move(e, window))

window.mainloop()