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
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.title("Login System")
        self.resizable(False,False)
        self.first_frame= tk.Frame(self,bg="blue")
        self.first_frame.pack(fill="both",expand=True)  

        app_icon = Image.open('image/icon.ico')
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)
           
        background = Image.open("image/cam.jpg")
        background = background.resize((1450, 700), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)

  
        tk.Label(self.first_frame,text="Login Here",font=("Impact",35,"bold"),fg="#d77337",bg="#DED461").place(x=90,y=30)
        tk.Label(self.first_frame,text="Accountant Emplyee Login Area",font=("Goudy old style",15,"bold"),fg="#d25d17",bg="#DED461").place(x=90,y=100)
        tk.Label(self.first_frame,text="Username",font=("Goudy old style",15,"bold"),fg="gray",bg="#DED461").place(x=90,y=140)
        
        
        self.txt_user=Entry(self.first_frame,font=("times new roman",15),bg="lightgray")
        
        self.txt_user.place(x=90,y=170,width=350,height=35)
        
        
        tk.Label(self.first_frame,text="Password",font=("Goudy old style",15,"bold"),fg="gray",bg="#DED461").place(x=90,y=210)

        self.txt_pass=tk.Entry(self.first_frame,font=("times new roman",15),bg="lightgray")
        self.txt_pass.place(x=90,y=240,width=350,height=35)

        tk.Button(self.first_frame,text="Create New Account",command=self.createAccount,cursor="hand2",bg="#DED461",fg="#d77337",bd=0,font=("times new roman",12)).place(x=90,y=280)
        tk.Button(self.first_frame,command=self.login_funtion,cursor="hand2",text="Login",fg="white",bg="#d77337",font=("times new roman",20)).place(x=300,y=470,width=180,height=40)\

        self.mainloop()

    def createAccount(self):
        msg=Tk()
        msg.geometry("380x500")
        msg.title("Create Account")
        msg.resizable(False,False)
        msg.configure(bg="white")        

     
        tk.Label(msg,text="Sign Up",font=("Impact",35,"bold"),fg="#d77337",bg="white").place(x=30,y=30)
        tk.Label(msg,text="It's quick and easy",font=("Goudy old style",15,"bold"),fg="#d25d17",bg="white").place(x=30,y=100)
        tk.Label(msg,text="Username",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=30,y=140)
                
                
        self.acc_user=Entry(msg,font=("times new roman",15),bg="lightgray")
                
        self.acc_user.place(x=30,y=170,width=300,height=35)
                
                
        tk.Label(msg,text="Password",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=30,y=210)

        self.acc_pass=tk.Entry(msg,font=("times new roman",15),bg="lightgray")
        self.acc_pass.place(x=30,y=240,width=300,height=35)

                
        tk.Button(msg,cursor="hand2",command=self.register_user,text="Sign Up",fg="white",bg="#d77337",font=("times new roman",20)).place(x=80,y=400,width=180,height=40)

        msg.mainloop()


    #-------------registe--------------------

    def checkRegister(self,nickname):
        for line in open("data/accounts.txt","r").readlines():
            account_info = line.split()
            if nickname==account_info[0]:
                return False
        return True

    def register_user(self):
        nickregister = self.acc_user.get()
        passregister = self.acc_pass.get()

        if (nickregister=='' or passregister==''):
                messagebox.showerror("Error","Invalid Username/Password")

        else:
            if self.checkRegister(nickregister)==True:
                file = open("data/accounts.txt","a")
                file.write(f"\n{nickregister} {passregister}")
                messagebox.showinfo("Congratulations","Your account has been registered")


            else:
                self.acc_pass.delete(0,END)
                self.acc_user.delete(0,END)
                messagebox.showerror("Error","Username already exists please enter new username username")
                
    #-------------login side-----------------   
    def checkLogin(self,nickname,password):
        for line in open("data/accounts.txt","r").readlines(): 
            login_info = line.split() 
            print(login_info[0],login_info[1])
            # print(nickname,password)
            if nickname == login_info[0] and password == login_info[1]:
                return True
        return False

    def login_funtion(self):
        nicknameClient=self.txt_user.get()
        passwordClient=self.txt_pass.get()
        
        
        if self.txt_pass.get()=="" or self.txt_user.get()=="":
            
            messagebox.showerror("Error","Invalid Username/Password")
        else:
            if self.checkLogin(nicknameClient,passwordClient)==1:
                
                Clinet(self,self.first_frame,nicknameClient,passwordClient,HOST,PORT)
            else:
                self.txt_user.delete(0, END)
                self.txt_pass.delete(0, END)
                messagebox.showerror("Error","Username or Password incorrect")
            






class Clinet(tk.Canvas):
    def __init__(self,parent,first_frame,txt_user,txt_pass,host,port):
        super().__init__(parent)
        self.window = 'ChatScreen'

        self.first_frame = first_frame
        self.first_frame.pack_forget()

        self.parent = parent

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        
        #----------------------menu--------------------
        menu = Menu(self)
        self.parent.config(menu=menu)
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
        app_icon = Image.open('image/icon.ico')
        app_icon = ImageTk.PhotoImage(app_icon)
       
        #SET BACKGROUND
        background = Image.open("image/backG.gif")
        background = background.resize((1450, 700), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        background1 = Image.open("image/backG1.jpg")
        background1 = background1.resize((1450, 700), Image.ANTIALIAS)
        self.background1 = ImageTk.PhotoImage(background1)
        background2 = Image.open("image/scenery.jpg")
        background2 = background2.resize((1450, 700), Image.ANTIALIAS)
        self.background2 = ImageTk.PhotoImage(background2)
        

        tk.Label(self.parent, image=self.background).place(x=0, y=0)

        #chat LABEL
        chat_label=Image.open("image/chat.jpg")
        chat_label=chat_label.resize((60,40),Image.ANTIALIAS)
        chat_label=ImageTk.PhotoImage(chat_label)
        tk.Label(self.parent,image=chat_label).pack()

        #BUTTON SEND
        send_label=Image.open("image/send.jpg")
        send_label=send_label.resize((50,50),Image.ANTIALIAS)
        send_label=ImageTk.PhotoImage(send_label)
        self.send_label = tk.Button(self.parent, image=send_label,command=self.write, borderwidth = 0)

        #Scream Chat
        chat_msg=Image.open("image/mess.jpg")
        chat_msg=chat_msg.resize((100,50),Image.ANTIALIAS)
        self.chat_msg=ImageTk.PhotoImage(chat_msg)
        
        self.nickname = txt_user
        self.password = txt_pass
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop) 
        receive_thread = threading.Thread(target = self.receive)
        gui_thread.start()
        receive_thread.start()
        self.mainloop()

    
    def gui_loop(self):
    

        self.text_area = tk.scrolledtext.ScrolledText(self.parent)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")
    
        tk.Label(self.parent,image=self.chat_msg).pack()

        self.input_area = tk.Text(self.parent, height=3)
        self.input_area.config(font=("Transformers Movie",10))
        self.input_area.pack(padx=20, pady=5)

 
        
        self.send_label.pack()
  
# Create button and image
        

        self.gui_done = True

        self.parent.protocol("WM_DELETE_WINDOW", self.stop)

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
        
        message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.parent.destroy()
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





FirstScreen()
