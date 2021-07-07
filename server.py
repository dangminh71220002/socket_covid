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
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)
clients=[]
nicknames=[] 
class FirstScreen(tk.Tk):
    def __init__(self,host,port):
        super().__init__()
        self.geometry("1200x600")
        self.resizable(False,False)
        self.first_frame = tk.Frame(self, bg="sky blue")
        self.first_frame.pack(fill="both", expand=True)
        background = Image.open("image/cam.jpg")
        background = background.resize((1200, 600), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)



        self.text_area = tk.scrolledtext.ScrolledText(self.first_frame)
        self.text_area.place(x=275,y=85)
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")

        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()
        tk.Label(self.first_frame,text="SERVER",font=("Impact",20,"bold"),fg="#d77337",bg="#DED461").place(x=570,y=20)
        tk.Label(self.first_frame,text="Client",font=("times new roman",15),fg="#d77337",bg="#DED461").place(x=93,y=90)
        tk.Label(self.first_frame,text="Kick CLient",font=("times new roman",15),fg="#d77337",bg="#DED461").place(x=1030,y=90)
        self.button_Kick=tk.Button(self.first_frame,cursor="hand2",text="Kick",fg="white",bg="#d77337",font=("times new roman",15,),).place(x=1050,y=200,width=60,height=30)
        
        self.text_user = tk.scrolledtext.ScrolledText(self.first_frame)
        self.text_user.config(state='disabled',fg="#00B7FE")
        self.text_user.configure(bg="white")
        self.text_user.place(x=30,y=136,width=200,height=200)


        self.input_kick = tk.Text(self.first_frame)
        self.input_kick.config(font=("Transformers Movie",10))
        self.input_kick.place(x=980, y=136,width=200,height=50)

        self.input = tk.Text(self.first_frame)
        self.input.config(font=("Transformers Movie",10))
        self.input.place(x=280, y=500,width=570,height=50)
        self.send=tk.Button(self.first_frame,cursor="hand2",text="send",fg="white",bg="#d77337",font=("times new roman",15,),command=self.ServerChat).place(x=870,y=500,width=60,height=50)
        self.mainloop()
        

               
    def broadcast(self,message):
        for client in clients:
            client.send(message)

    def handle(self,client): 
         while True :
            try:
                thread2 = threading.Thread(target=self.ServerChat,args=(server, ))
                thread2.start() 
                    
                message=client.recv(1024)
                self.text_area.config(state='normal')
                self.text_area.insert('end',"User chat\n")
                self.text_area.insert('end',message)
                self.text_area.yview('end')
                self.text_area.config(state='disabled')     
                self.broadcast(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname=nicknames[index]
                nicknames.remove(nickname)
                break
    def ServerChat(self,client):
        index=self.input.get('1.0','end')
        self.input.delete('1.0','end')
        inp="server: "+index+"\n"
        self.text_area.config(state='normal')
        self.text_area.insert('end',inp)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.broadcast(inp.encode('utf-8'))


    #-------Login--------
    def checkLogin(self,nickname,password):
        for line in open("data/accounts.txt","r").readlines():
            login_info = line.split()
            if nickname == login_info[0] and password == login_info[1]:
                return True
        return False    

    def ProcessLogin(self,nickname,password,client,address):
        if self.checkLogin(nickname,password) == True:
            client.send('true'.encode('utf-8'))
            nicknames.append(nickname)    
            clients.append(client) 
            self.text_area.config(state='normal')
            self.text_area.insert('end',"User login\n")
            self.text_area.insert('end',f"Nick:{nickname}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')



            self.text_area.config(state='normal')
            self.text_area.insert('end',f"NICKNAME of  the clients is: {nickname}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')


            self.broadcast(f"{nickname} connected to server \n".encode('utf-8'))
            client.send(f"Connected to server \n".encode("utf-8"))
            thread1 = threading.Thread(target= self.handle, args=(client,) )
            thread1.start()
        else:
            client.send('wrong_pass'.encode('utf-8'))
            self.text_area.config(state='normal')
            self.text_area.insert('end',f"{address} disconnected\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            client.close()

    #========register=========
    def checkRegister(self,nickname,password):
        for line in open("data/accounts.txt","r").readlines():
            account_info = line.split()
            if nickname==account_info[0]:
                return False
        return True

    def ProcessRegister(self,nickname,password,client,address):
        if self.checkRegister(nickname,password)==True:
            client.send('complete'.encode('utf-8'))
            file = open("data/accounts.txt","a")
            file.write(f"\n{nickname} {password}")

            self.text_area.config(state='normal')
            self.text_area.insert('end',"User register\n")
            self.text_area.insert('end',f"Nick:{nickname}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
        else:
            client.send('exists'.encode('utf-8'))
            self.text_area.config(state='normal')
            self.text_area.insert('end',f"{address} disconnected\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            client.close()


    def receive(self):
        while True:
            client,address  =server.accept()

            self.text_area.config(state='normal')
            self.text_area.insert('end',f"Connected with{str(address)}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

            if len(clients)==5:
                client.send('not_allowed'.encode())
                
                continue
            else:
                client.send('allowed'.encode())
            try:
                nickname= client.recv(1024).decode('utf-8')
                password= client.recv(1024).decode('utf-8')
                option  = client.recv(1024).decode('utf-8')
                print(option)
            except:
                self.text_area.config(state='normal')
                self.text_area.insert('end',f"{address} disconnected\n")
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
                client.close()
                continue
            if option=='login': self.ProcessLogin(nickname,password,client,address)
            if option=='register': self.ProcessRegister(nickname,password,client,address)

            
       
FirstScreen(HOST,PORT)