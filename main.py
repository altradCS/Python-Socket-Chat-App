import customtkinter as ctk
from function import *
import tkinter as tk
from tkinter import ttk
from client_origin import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import server
# from client_origin import *
class client_ui():
    def __init__(self,root):
        global close_img, maximize, minimize, menu_img, add,client_device,user_image, image_send
        self.number_of_client=0
        self.frame_dict = {}
        self.buttons = {}
        self.server_status = True

        
        menu_img = get_img("assets\icon_app.png", 40,40)
        add =ctk.CTkImage(Image.open("assets\icons8-plus-50.png"),size=(30,30))
        client_device = ctk.CTkImage(Image.open("assets/icons8-cloud-computing-50.png"), size=(30,30))#get_img("assets/icons8-cloud-computing-50.png", 35,35)
        user_image = get_img("assets/icons8-user-48.png", 35, 35)
        image_send = ctk.CTkImage(Image.open("assets/icons8-send-50.png"),size=(30,30))
        self.start_img = ctk.CTkImage(Image.open("assets\icons8-play-50.png"), size=(15,15))
        self.stop_img = ctk.CTkImage(Image.open("assets\icons8-stop-50.png"), size=(15,15))

        self.root = root
        self.top_win = tk.Toplevel(window)
        self.top_win.wm_attributes("-alpha", 0.0)
        self.top_win.bind("<Map>", lambda e: onRootDeiconify(self.root))
        self.top_win.bind("<Unmap>", lambda e: minimize_window(root, self.top_win))
        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.title("Client")
        self.root.overrideredirect(True)
        self.root.geometry("825x530")
        #title frame
        self.top_bar = tk.Frame(self.root, bg="#333333", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_bar.grid_columnconfigure(1, weight=1)
        #add side frame
        self.side_frame = ctk.CTkFrame(self.root, corner_radius=0,fg_color="#333333")
        self.side_frame.grid(row=1, column=0, sticky="nsew")
        #add middle frame
        self.middle_frame = ctk.CTkFrame(self.root, fg_color="#242424", corner_radius=0)
        self.middle_frame.grid(row=1, column=1, sticky="nsew")
        self.menu = tk.Button(self.top_bar,
                                text=' ConnectedZ',
                                image= menu_img,
                                bg="#333333",
                                activebackground="#333333",
                                activeforeground="white",
                                relief='flat',
                                border=0,
                                font=("Roboto mono", 15, "bold"),
                                fg="white",
                                compound=tk.LEFT,
                                command=lambda: close_win(root),
                                )
        self.menu.grid(row=0, column=0, padx=10)
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
        
        self.title_frame = ctk.CTkFrame(self.top_bar,fg_color="#333333", corner_radius=0)
        self.title_frame.grid(row=0, column=2)


        #server button
        self.server_button = ctk.CTkButton(self.title_frame,
                                           image=self.start_img,
                                           text="Start Server",
                                           fg_color="#333333",
                                           hover_color="#02733E",
                                           border_color="#02733E",
                                           border_width=2,
                                           width=40,
                                           font=("JetBrains Mono", 12,"bold"),
                                           compound=tk.LEFT,
                                           command=lambda: start_stop_server(self))
        self.server_button.grid(row=0, column=0, sticky="w", padx=20)


        # get icons for control frame
        close_img = ctk.CTkImage(Image.open("assets/x.png"),size=( 25,26))
        maximize = ctk.CTkImage(Image.open("assets/maximize-2_white.png"),  size=(25,26))
        minimize = ctk.CTkImage(Image.open("assets/minus_white.png"),  size=(25,26))
        self.close = ctk.CTkButton(self.title_frame,
                                   text="",
                               image= close_img,
                               fg_color="#333333",
                               hover_color="red",
                               corner_radius=0,
                               command=lambda: close_win(root),
                               width=40)
        self.close.grid(row=0, column=3)
        self.minimize = ctk.CTkButton(self.title_frame,
                                  image=minimize,
                                  fg_color="#333333",
                                  hover_color="grey",
                                  corner_radius=0,
                                  text="",
                                  command=lambda: minimize_window(root, self.top_win),
                                  width=40)
        self.minimize.grid(row=0, column=1)
        self.maximize = ctk.CTkButton(self.title_frame,
                                  image= maximize,
                                  fg_color="#333333",
                                  hover_color="grey",
                                  corner_radius=0,
                                  text="",
                                  command=lambda: maximize_win(self,root),
                                  width=40)
        self.maximize.grid(row=0, column=2)
        self.prompt_label = ctk.CTkLabel(self.middle_frame, text="Press + to connect to the server", font=("JetBrains Mono",20, "italic"))
        self.prompt_label.pack(fill="none", expand=True)



    def add_client_device(self):

        self.prompt_label.destroy()
        ask_info = ctk.CTkToplevel(self.root)
        ask_info.title("Client Information")
        ask_info.geometry("300x200")
        name = ctk.CTkEntry(ask_info, font=("JetBrains Mono", 12))
        name.pack(fill="x", expand=True)
        email = ctk.CTkEntry(ask_info, font=("JetBrains Mono", 12))
        email.pack(fill="x", expand=True)
        password = ctk.CTkEntry(ask_info, font=("JetBrains Mono", 12))
        password.pack(fill="x", expand=True)
        submit = ctk.CTkButton(ask_info, text="Submit", font=("JetBrains Mono", 12), command=lambda: self.add_client(name.get(), email.get(), password.get(), ask_info))

        submit.pack(fill="x", expand=True)
    def add_client(self, name, email, password, ask_info):
        
        connection = connect()
        connection.send(name.encode(FORMAT))

        self.buttons[email]=ctk.CTkButton(self.side_frame,
                                        text="",
                                        fg_color="#333333",
                                        hover_color="#114AAF",
                                        width=40,
                                        image=client_device,
                                        compound=tk.LEFT,
                                        
                                        )
        self.buttons[email].configure(command=lambda name = self.buttons[email]: create_new_frame(self,name, email,connection, user_image, image_send))
        # create_button(self.buttons[name])
        self.buttons[email].grid(row=self.number_of_client+1,column=0)
        self.number_of_client += 1
        ask_info.destroy()

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



    
if __name__ == "__main__":
    #threading.Thread(target=server.start).start()
    window = ctk.CTk()
    Ui =client_ui(window)
    Ui.top_bar.bind('<Button-1>', lambda e: origin_cords(e, window))
    Ui.top_bar.bind('<B1-Motion>', lambda e: move(e, window))
    window.mainloop()