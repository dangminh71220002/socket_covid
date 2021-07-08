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
import urllib, json
import urllib.request as ur

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
        #set BackGround
        background = Image.open("image/cam.jpg")
        background = background.resize((1200, 600), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)


        #Text area chat of clientS and server
        self.text_area = tk.scrolledtext.ScrolledText(self.first_frame)
        self.text_area.place(x=475,y=85)
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")
        

        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()
        #---------Lable------------------
        tk.Label(self.first_frame,text="SERVER",font=("Impact",20,"bold"),fg="#d77337",bg="#DED461").place(x=570,y=20)
        tk.Label(self.first_frame,text="Client",font=("times new roman",15),fg="gray",bg="#DED461").place(x=40,y=110)
        tk.Label(self.first_frame,text="Kick Client",font=("times new roman",15),fg="gray",bg="#DED461").place(x=40,y=370)
        tk.Label(self.first_frame,text="Chat",font=("times new roman",15),fg="gray",bg="#DED461").place(x=480,y=50)
        #===================================================
        #button Kick clients
        self.button_Kick=tk.Button(self.first_frame,cursor="hand2",text="KICK",fg="white",bg="#d77337",font=("times new roman",15),command=self.writeKick).place(x=200,y=480,width=60,height=30)
        #text area status of client
        self.text_user = tk.scrolledtext.ScrolledText(self.first_frame)
        self.text_user.config(state='disabled',fg="#00B7FE")
        self.text_user.configure(bg="white")
        self.text_user.place(x=30,y=136,width=400,height=200)

        #Enter name of client server want Kick
        self.input_kick = tk.Text(self.first_frame)
        self.input_kick.config(font=("Transformers Movie",10))
        self.input_kick.place(x=30, y=400,width=400,height=50)
        #Enter mess of server to client
        self.input = tk.Text(self.first_frame)
        self.input.config(font=("Transformers Movie",10))
        self.input.place(x=475, y=500,width=570,height=50)
        self.send=tk.Button(self.first_frame,cursor="hand2",text="SEND",fg="white",bg="#d77337",font=("times new roman",15,),command=self.ServerChat).place(x=1070,y=500,width=60,height=50)
        thread2 = threading.Thread(target=self.ServerChat,args=( ))
        thread2.start() 
        
        self.mainloop()

#--------------- function of KICK
    def kickClient(self,name):
        if name in nicknames:
            name_index= nicknames.index(name)
            client_kick=clients[name_index]
            clients.remove(client_kick)       
            client_kick.send("You were kicked by admin ".encode('utf-8'))   
            client_kick.close()
            nicknames.remove(name)
        

    def writeKick(self):
        name_kick=self.input_kick.get('1.0','end-1c')
        self.name_kick=name_kick
        self.input_kick.delete('1.0','end')
        self.kickClient(name_kick)
        

#================================
# send mess of server to clients          
    def broadcast(self,message):
        for client in clients:
            
            client.send(message)

    def getdataCovid(self):
        url = 'https://coronavirus-19-api.herokuapp.com/countries'
        response = ur.urlopen(url)
        data = json.loads(response.read())
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def commandCovid(self):
        self.getdataCovid()

    def getCountry(self,client):
        f= open('data.json',)
        data = json.load(f)
        num =0
        mess=''
        for i in data:
            if (num==0): num+=1
            else:
                if num==6:
                    mess+=i['country']+'.\n'
                    client.send(mess.encode('utf-8'))
                    mess=''
                    num=1
                else:
                    mess+=i['country']+' , '
                    num+=1

    def handle(self,client): 
         while True :
            try:
                message = client.recv(1024).decode('utf-8')
                temp = message.split(':')
                covid = 'covid'
                country = 'country'
                if temp[1][1]!='/':
                    self.text_area.config(state='normal')
                    self.text_area.insert('end',"User chat\n")
                    self.text_area.insert('end',message)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
                    self.broadcast(message.encode('utf-8'))
                else:
                    if country in temp[1]:
                        self.getCountry(client)
                    if (covid in temp[1]):
                        print('456')
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname=nicknames[index]
                nicknames.remove(nickname)
                break
    #mess's server send to client
    def ServerChat(self):
        index=self.input.get('1.0','end')
        if index!='\n':
            self.input.delete('1.0','end')
            inp="server: "+index
            self.text_area.config(state='normal')
            self.text_area.insert('end',inp)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            self.broadcast(inp.encode('utf-8'))
        

    def stop(self):
        self.first_frame.destroy()
        server.close()
        exit(0)


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

            self.text_user.config(state='normal')
            self.text_user.insert('end',f"User:{nickname}\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')

            self.text_user.config(state='normal')
            self.text_user.insert('end',f"NICKNAME of  the clients is: {nickname}\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')


            self.broadcast(f"{nickname} connected to server \n".encode('utf-8'))
            client.send(f"Connected to server \n".encode("utf-8"))
            thread1 = threading.Thread(target= self.handle, args=(client,) )
            thread1.start()
        else:
            client.send('wrong_pass'.encode('utf-8'))
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{address} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
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
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{address} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client.close()


    def receive(self):
        while True:
            client,address  =server.accept()

            self.text_user.config(state='normal')
            self.text_user.insert('end',f"Connected with{str(address)}\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')

            if len(clients)==5:
                client.send('not_allowed'.encode())
                
                continue
            else:
                client.send('allowed'.encode())
            try:
                nickname= client.recv(1024).decode('utf-8')
                password= client.recv(1024).decode('utf-8')
                option  = client.recv(1024).decode('utf-8')
                print(option,nickname,password)
            except:
                self.text_user.config(state='normal')
                self.text_user.insert('end',f"{address} disconnected\n")
                self.text_user.yview('end')
                self.text_user.config(state='disabled')
                client.close()
                continue
            if option=='login': self.ProcessLogin(nickname,password,client,address)
            if option=='register': self.ProcessRegister(nickname,password,client,address)

            
       
FirstScreen(HOST,PORT)