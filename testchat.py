import socket
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pickle
from datetime import datetime
import os
import threading
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PIL import Image,ImageTk
import emoji
import tkinter as tk

HOST = '127.0.0.1'
PORT = 80

class FirstScreen(tk.Tk):
    def __init__(self,host,port):
        super().__init__()
        self.geometry("1000x600")
        self.title("CHAT")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        self.first_frame = tk.Frame(self, bg="sky blue")
        self.first_frame.pack(fill="both", expand=True)
        #----------------------menu--------------------
        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="White-Blue Sky", command=self.backG1)
        file.add_command(label="Black-White",command=self.backG2)
        file.add_command(label="Green-Red",command=self.backG)
        menu.add_cascade(label="Change Background", menu=file)
        
        edit = Menu(menu)
        edit.add_command(label=emoji.emojize("\U00002665"), command=self.print_heart)
        edit.add_command(label=emoji.emojize("\U0001F62D"), command=self.print_cry)
        edit.add_command(label=emoji.emojize("\U0001F604"), command=self.print_facesmile)
        edit.add_command(label=emoji.emojize("\U0001F97A"), command=self.sadface)
        menu.add_cascade(label="Emoji", menu=edit)
    #-----------------------------------------------------------------------------------
        app_icon = Image.open('icon.ico')
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)
        #SET BACKGROUND
        background = Image.open("backG.gif")
        background = background.resize((1450, 700), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        background1 = Image.open("backG1.jpg")
        background1 = background1.resize((1450, 700), Image.ANTIALIAS)
        self.background1 = ImageTk.PhotoImage(background1)
        background2 = Image.open("scenery.jpg")
        background2 = background2.resize((1450, 700), Image.ANTIALIAS)
        self.background2 = ImageTk.PhotoImage(background2)
        

        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)

        #chat LABEL
        chat_label=Image.open("chat.jpg")
        chat_label=chat_label.resize((60,40),Image.ANTIALIAS)
        chat_label=ImageTk.PhotoImage(chat_label)
        tk.Label(self.first_frame,image=chat_label).pack()

        #BUTTON SEND
        send_label=Image.open("send.jpg")
        send_label=send_label.resize((50,50),Image.ANTIALIAS)
        send_label=ImageTk.PhotoImage(send_label)
        self.send_label = tk.Button(self.first_frame, image=send_label,command=self.write, borderwidth = 0)

        #Scream Chat
        chat_msg=Image.open("mess.jpg")
        chat_msg=chat_msg.resize((100,50),Image.ANTIALIAS)
        self.chat_msg=ImageTk.PhotoImage(chat_msg)
        
        self.nickname = simpledialog.askstring("Nickname", "Please choose a Nickname", parent=self.first_frame)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop) 
        receive_thread = threading.Thread(target = self.receive)
        gui_thread.start()
        receive_thread.start()
        self.mainloop()

    
    def gui_loop(self):
    

        self.text_area = tk.scrolledtext.ScrolledText(self.first_frame)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")
    
        tk.Label(self.first_frame,image=self.chat_msg).pack()

        self.input_area = tk.Text(self.first_frame, height=3)
        self.input_area.config(font=("Transformers Movie",10))
        self.input_area.pack(padx=20, pady=5)

 
        
        self.send_label.pack()
  
# Create button and image
        

        self.gui_done = True

        self.protocol("WM_DELETE_WINDOW", self.stop)

    def backG1(self):
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")
    def backG2(self):
        self.text_area.config(state='disabled',fg="white")
        self.text_area.configure(bg="black")
    def backG(self):
        self.text_area.config(state='disabled',fg="#FE0E1D")
        self.text_area.configure(bg="#02FF6F")
    def print_heart(self) :
        heart="\U00002665"
        message = f"{self.nickname} : {heart} \n"
        self.sock.send(message.encode('utf-8'))
    def print_facesmile(self) :
        face="\U0001F604"
        message = f"{self.nickname} : {face} \n"
        self.sock.send(message.encode('utf-8')) 
    def print_cry(self) :
        cry="\U0001F62D"
        message = f"{self.nickname} : {cry} \n"
        self.sock.send(message.encode('utf-8'))
    def sadface(self) :
        heart="\U0001F97A"
        message = f"{self.nickname} : {heart} \n"
        self.sock.send(message.encode('utf-8'))
    def write(self):
        
        message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.first_frame.destroy()
        self.sock.close()
        exit(0)

        

    def receive(self):  
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break  





FirstScreen(HOST,PORT)