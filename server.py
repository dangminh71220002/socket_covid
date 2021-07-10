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
import time

from threading import Timer
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
import hashlib
HOST = '127.0.0.1'
PORT = 80
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)
clients=[]
nicknames=[] 
stop = False
One = True
isServerstop = False
Kick = False
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
        
        menu = Menu(self)
        self.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Close server")
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
        self.protocol("WM_DELETE_WINDOW",self.stop)
        self.mainloop()

#--------------- function of KICK-------------------------
    def kickClient(self,name):
        global Kick
        if name in nicknames:
            Kick = True
            name_index= nicknames.index(name)
            client_kick=clients[name_index]
            clients.remove(client_kick)
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{name} were KICK\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client_kick.send("You were kicked by admin ".encode('utf-8'))   
            client_kick.close()
            nicknames.remove(name)
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{name} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            self.broadcast(f"{name} disconnect server".encode('utf-8'))
        

    def writeKick(self):
        name_kick=self.input_kick.get('1.0','end-1c')
        self.name_kick=name_kick
        self.input_kick.delete('1.0','end')
        self.kickClient(name_kick)
        

#===========================================================
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
                    mess+=i['country']+','
                    num+=1

    def getInfoCovid(self,client,region):
        regionTemp = region
        region = urllib.parse.quote(region)
        url = f"https://coronavirus-19-api.herokuapp.com/countries/{region}"
        try:
            response = ur.urlopen(url)
            data = json.loads(response.read())
            covid = f'''{regionTemp} covid figures
Total cases : {data['cases']}
Today cases : {data['todayCases']}
Deaths : {data['deaths']}
Recover: {data['recovered']}\n'''
            client.send(covid.encode('utf-8'))
        except:
            client.send(f"{regionTemp} covid figures could be found\n".encode('utf-8'))

    def set_interval(self,func, sec):
        sectemp = 0.1
        i=1
        while True:
            func()
            while (i<=sec/0.1): 
                time.sleep(sectemp)
                i+=1
            i=1
        

    def update(self):
        url = f"https://coronavirus-19-api.herokuapp.com/countries"
        if len(nicknames)==0: return "out"
        self.text_area.config(state='normal')
        self.text_area.insert('end',"Server update covid figures\n")
        
        try:
            response = ur.urlopen(url)
            data = json.loads(response.read())
            with open('data.json', 'w') as f:
                json.dump(data, f)
            
            self.text_area.insert('end',f"Done\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
        except:
            self.text_area.insert('end',f"Error\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

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
                    if covid in temp[1]:
                        # print(temp[1][8:len(temp[1])-1])

                        region = temp[1][8:len(temp[1])-1]
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',"User search covid\n")
                        self.text_area.insert('end',f"Region :{region}\n")
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                        self.getdataCovid()
                        self.getInfoCovid(client,region)
            except:
                global Kick
                if Kick==False:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname=nicknames[index]
                    self.text_user.config(state='normal')
                    self.text_user.insert('end',f"{nickname} disconnected\n")
                    self.text_user.yview('end')
                    self.text_user.config(state='disabled')
                    self.broadcast(f"{nickname} disconnect server".encode('utf-8'))
                    nicknames.remove(nickname)
                Kick = False
                break
        
    #mess's server send to client
    def ServerChat(self):
        index=self.input.get('1.0','end')
        if index!='\n':
            global isServerstop
            global server

            if index == '/close\n':
                
                isServerstop= True
                self.broadcast('Server offline'.encode('utf-8'))
                for client in clients:
                    global Kick
                    Kick = True
                    client.close()
                Kick = True
                clients.clear()
                nicknames.clear()
                if (One==True):
                    time.sleep(0)
                server.close()
            elif index == '/start\n':

                if isServerstop==True:
                    isServerstop= False
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.bind((HOST,PORT))
                    server.listen(5)
                    receive_thread = threading.Thread(target = self.receive)
                    receive_thread.start()
                else:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end',"Server doesn't close\n")
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
            else:
                self.input.delete('1.0','end')
                inp="server: "+index
                self.text_area.config(state='normal')
                self.text_area.insert('end',inp)
                self.text_area.yview('end')
                self.text_area.config(state='disabled')
                self.broadcast(inp.encode('utf-8'))

        

    def stop(self):
        # thread2.kill()
        global isServerstop
        if (isServerstop==0):
            messagebox.showerror("Error","Stop server before close Window")
        else:
        # global stop,CW,One
        # global thread1
        # stop = True
        # if (CW==True):
        #     if (thread1.is_alive()): thread1.join()
        #     print("kill threading")
        # if (One==True):
        #     time.sleep(0)
            self.first_frame.destroy()
        # server.close()
            exit(0)


    #-------Login--------
    def checkLogin(self,nickname,password):
        salt = "5gz"
        check_password = password+salt
        check_password = hashlib.md5(check_password.encode())
        for line in open("data/accounts.txt","r").readlines():
            login_info = line.split()
            
            if nickname == login_info[0] and check_password.hexdigest() == login_info[1]:
                return True
        return False    

    def ProcessLogin(self,nickname,password,client,address):
        if self.checkLogin(nickname,password) == True:
            
            if nickname in nicknames:
                client.send('logged'.encode('utf-8'))
                self.text_user.config(state='normal')
                self.text_user.insert('end',f"{address} disconnected\n")
                self.text_user.yview('end')
                self.text_user.config(state='disabled')
                client.close()
                return
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
        salt = "5gz"
        
        for line in open("data/accounts.txt","r").readlines():
            account_info = line.split()
            if nickname==account_info[0]:
                return False
        return True

    def ProcessRegister(self,nickname,password,client,address):
        if self.checkRegister(nickname,password)==True:
            client.send('complete'.encode('utf-8'))
            file = open("data/accounts.txt","a")
            salt = "5gz"
            reg_password = password+salt
            reg_password = hashlib.md5(reg_password.encode())
            file.write(f"\n{nickname} {reg_password.hexdigest()}")

            self.text_area.config(state='normal')
            self.text_area.insert('end',"User register\n")
            self.text_area.insert('end',f"Nick:{nickname}\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
            client.close()
        else:
            client.send('exists'.encode('utf-8'))
            self.text_user.config(state='normal')
            self.text_user.insert('end',f"{address} disconnected\n")
            self.text_user.yview('end')
            self.text_user.config(state='disabled')
            client.close()


    def receive(self):
        try: 
            global One
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
                    # print(option,nickname,password)
                except:
                    self.text_user.config(state='normal')
                    self.text_user.insert('end',f"{address} disconnected\n")
                    self.text_user.yview('end')
                    self.text_user.config(state='disabled')
                    client.close()
                    break
                    continue
                if option=='login': self.ProcessLogin(nickname,password,client,address)
                if option=='register': self.ProcessRegister(nickname,password,client,address)
                if len(nicknames)>0 and One == True: 
                    t = threading.Thread(target=self.set_interval,args=(self.update,10,), daemon=True)
                    t.start()
                    One = False

        except socket.error:
            print("Shutting down")
            

            
       
FirstScreen(HOST,PORT)