import socket
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from datetime import datetime
import threading
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PIL import Image,ImageTk
import tkinter as tk
from datetime import datetime


PORT = 80

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
class FirstScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        # screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.x_co = int((screen_width / 2) - (1000 / 2))
        # self.y_co = int((screen_height / 2) - (600 / 2)) - 80
        # self.geometry(f"1000x600+{self.x_co}+{self.y_co}")
        
        self.geometry("1000x600")
        self.title("Login System")
        self.resizable(False,False)
        self.first_frame= tk.Frame(self,bg="blue")
        self.first_frame.pack(fill="both",expand=True)  
        #ICON
        app_icon = Image.open('image/clientlogo.jpg')
        app_icon = ImageTk.PhotoImage(app_icon)
        self.iconphoto(False, app_icon)
        #BACKGROUND
        background = Image.open("image/cam2.jpg")
        background = background.resize((1000, 600), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
        tk.Label(self.first_frame, image=self.background).place(x=0, y=0)


        tk.Label(self.first_frame,text="Login Here",font=("Impact",35,"bold"),fg="#d77337",bg="#FAFAFA").place(x=90,y=30)
        tk.Label(self.first_frame,text="Accountant Emplyee Login Area",font=("Goudy old style",15,"bold"),fg="#d25d17",bg="#FAFAFA").place(x=90,y=100)
        tk.Label(self.first_frame,text="Username",font=("Goudy old style",15,"bold"),fg="gray",bg="#FAFAFA").place(x=90,y=140)
        
        #Enter User
        self.txt_user=Entry(self.first_frame,font=("times new roman",15),bg="lightgray")
        self.txt_user.place(x=90,y=170,width=350,height=35)
        
        
        tk.Label(self.first_frame,text="Password",font=("Goudy old style",15,"bold"),fg="gray",bg="#FAFAFA").place(x=90,y=210)
        #Enter Pass
        self.txt_pass=tk.Entry(self.first_frame,show="*",font=("times new roman",15),bg="lightgray")
        self.txt_pass.place(x=90,y=240,width=350,height=35)

        tk.Label(self.first_frame,text="IP",font=("Goudy old style",15,"bold"),fg="gray",bg="#FAFAFA").place(x=90,y=275)

        self.txt_ip=Entry(self.first_frame,font=("times new roman",15),bg="lightgray")
        self.txt_ip.place(x=90,y=300,width=355,height=35)

        tk.Button(self.first_frame,text="Create New Account",command=self.createAccount,cursor="hand2",bg="#FAFAFA",fg="#d77337",bd=0,font=("times new roman",12)).place(x=90,y=360)
        tk.Button(self.first_frame,command=self.login_funtion,cursor="hand2",text="Login",fg="white",bg="#d77337",font=("times new roman",20)).place(x=300,y=470,width=180,height=40)

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
                
        #create User   
        self.acc_user=Entry(msg,font=("times new roman",15),bg="lightgray")
                
        self.acc_user.place(x=30,y=170,width=300,height=35)
                
                
        tk.Label(msg,text="Password",font=("Goudy old style",15,"bold"),fg="gray",bg="white").place(x=30,y=210)
        #create Pass
        self.acc_pass=tk.Entry(msg,show="*",font=("times new roman",15),bg="lightgray")
        self.acc_pass.place(x=30,y=240,width=300,height=35)

        tk.Label(msg,text="IP",font=("Goudy old style",15,"bold"),fg="gray",bg="#FAFAFA").place(x=30,y=280)
        self.acc_ip=Entry(msg,font=("times new roman",15),bg="lightgray")
        self.acc_ip.place(x=30,y=310,width=300,height=35)
        tk.Button(msg,cursor="hand2",command=self.register_user,text="Sign Up",fg="white",bg="#d77337",font=("times new roman",20)).place(x=80,y=360,width=180,height=40)
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
        HOST = self.acc_ip.get()
        if (nickregister=='' or passregister==''):
                messagebox.showerror("Error","Invalid Username/Password")

        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((HOST,PORT))
                status = client.recv(1024).decode('utf-8')
                if status == 'not_allowed':
                    client.close()
                    messagebox.showinfo(title="Can't connect !", message='Sorry, server is completely occupied.'
                                                                         'Try again later')
                    return
            except ConnectionRefusedError:
                messagebox.showinfo(title="Can't connect !", message="Server is offline , try again later.")
                print("Server is offline , try again later.")
                return
            nickregister= f'2{nickregister}'

            client.send(nickregister.encode('utf-8'))
            client.send(passregister.encode('utf-8'))
            
            result = client.recv(1024).decode('utf-8')
            if result == 'exists':
                self.txt_user.delete(0, END)
                self.txt_pass.delete(0, END)
                messagebox.showerror("Error","Username already exists")
                client.close()
            else:
                messagebox.showinfo("Congratulations","Successful account registration")
                client.close()




            # if self.checkRegister(nickregister)==True:
            #     file = open("data/accounts.txt","a")
            #     file.write(f"\n{nickregister} {passregister}")
            #     messagebox.showinfo("Congratulations","Your account has been registered")


            # else:
            #     self.acc_pass.delete(0,END)
            #     self.acc_user.delete(0,END)
            #     messagebox.showerror("Error","Username already exists please enter new username username")
                
    #-------------login side-----------------   

    def login_funtion(self):
        nicknameClient=self.txt_user.get()
        passwordClient=self.txt_pass.get()
        HOST = self.txt_ip.get()

        if HOST =='':
            messagebox.showerror("Error","Invalid IP")

        if nicknameClient=="" or passwordClient=="":        
            messagebox.showerror("Error","Invalid Username/Password")
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect((HOST,PORT))
                status = client.recv(1024).decode('utf-8')
                if status == 'not_allowed':
                    client.close()
                    messagebox.showinfo(title="Can't connect !", message='Sorry, server is completely occupied.'
                                                                         'Try again later')
                    return
            except ConnectionRefusedError:
                messagebox.showinfo(title="Can't connect !", message="Server is offline , try again later.")
                print("Server is offline , try again later.")
                return
            except socket.gaierror:
                messagebox.showerror(title="Error", message="Error IP")

            nicknameClient= f'1{nicknameClient}'
            client.send(nicknameClient.encode('utf-8'))
            client.send(passwordClient.encode('utf-8'))
            nicknameClient = nicknameClient[1:]

            result = client.recv(1024).decode('utf-8')
            print(result)
            if result == 'wrong_pass':
                self.txt_user.delete(0, END)
                self.txt_pass.delete(0, END)
                messagebox.showerror("Error","Username or Password incorrect")
                client.close()
            else:
                if result == 'logged':
                    self.txt_user.delete(0, END)
                    self.txt_pass.delete(0, END)
                    messagebox.showerror("Error","Username is logged in")
                    client.close()
                else: Clinet(self, self.first_frame,client,nicknameClient,passwordClient,HOST,PORT)
            # if self.checkLogin(nicknameClient,passwordClient)==1:
                
            #     Clinet(self,self.first_frame,nicknameClient,passwordClient,HOST,PORT)
            # else:
            #     self.txt_user.delete(0, END)
            #     self.txt_pass.delete(0, END)
            #     messagebox.showerror("Error","Username or Password incorrect")
            






class Clinet(tk.Canvas):
    def __init__(self, parent, first_frame,client,txt_user,txt_pass,host,port):
        super().__init__(parent)
        self.window = 'ChatScreen'

        self.first_frame = first_frame
        self.first_frame.pack_forget()
        self.sock = client
        self.parent = parent
        self.parent.bind('<Return>', lambda e: self.write(e))
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()

        x_co = int((screen_width / 2) - (1010 / 2))
        y_co = int((screen_height / 2) - (650 / 2)) - 80
        self.parent.geometry("1000x600")
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect((host,port))
        
        #----------------------menu--------------------
        menu = Menu(self)
        self.parent.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="White-Blue Sky", command=self.backG1)
        file.add_command(label="Black-White",command=self.backG2)
        file.add_command(label="Green-Red",command=self.backG)
        menu.add_cascade(label="Change Background", menu=file)
        
        # edit = Menu(menu)
        # edit.add_command(label=emoji.emojize("\U00002665"), command=self.print_heart)
        # edit.add_command(label=emoji.emojize("\U0001F62D"), command=self.print_cry)
        # edit.add_command(label=emoji.emojize("\U0001F604"), command=self.print_facesmile)
        # edit.add_command(label=emoji.emojize("\U0001F97A"), command=self.sadface)
        # menu.add_cascade(label="Emoji", menu=edit)
        User_manual=Menu(menu)
        User_manual.add_command(label="User manual",command=self.User_manual)
        menu.add_cascade(label="User manual", menu=User_manual)
    #-----------------------------------------------------------------------------------
     
       


        #SET BACKGROUND
        background = Image.open("image/covid.jpg")
        background = background.resize((1450, 700), Image.ANTIALIAS)
        self.background = ImageTk.PhotoImage(background)
       
        
        tk.Label(self, image=self.background).place(x=0, y=0)


        #BUTTON SEND
        send_label=Image.open("image/send.jpg")
        send_label=send_label.resize((50,50),Image.ANTIALIAS)
        send_label=ImageTk.PhotoImage(send_label)
        self.send_label = tk.Button(self, image=send_label,command=self.write, borderwidth = 0)

        out_label=Image.open("image/loout.jpg")
        out_label=out_label.resize((30,30),Image.ANTIALIAS)
        out_label=ImageTk.PhotoImage(out_label)
        self.out_label=tk.Button(self, image=out_label,command=self.on_closing, borderwidth = 0,bg="#2E353E")

        #Scream Chat
        chat_msg=Image.open("image/covidmini.jpg")
        chat_msg=chat_msg.resize((50,50),Image.ANTIALIAS)
        self.chat_msg=ImageTk.PhotoImage(chat_msg)
#----------------------------------SET COUNTRY---------------------------------------------
#combo=ttk.Combobox(self.parent)
        self.combo =ttk.Combobox(self)

        self.combo['values']= ("World","USA","India","Brazil","France","Russia",
        "Turkey","UK","Argentina","Colombia","Italy","Spain","Germany",
        "Iran","Poland","Mexico","Indonesia","Ukraine","South Africa",
        "Peru","Netherlands","Czechia","Chile","Philippines","Canada",
        "Iraq","Sweden","Belgium","Romania","Bangladesh","Pakistan",
        "Portugal","Israel","Japan","Hungary","Malaysia","Jordan",
        "Serbia","Switzerland","Austria","Nepal","UAE","Lebanon",
        "Morocco","Saudi Arabia","Ecuador","Tunisia","Bolivia","Kazakhstan",
        "Paraguay","Greece","Belarus","Bulgaria","Panama","Slovakia",
        "Costa Rica","Uruguay","Georgia","Kuwait","Croatia","Azerbaijan",
        "Dominican Republic","Palestine","Guatemala","Thailand","Denmark","Egypt",
        "Venezuela","Oman","Lithuania","Ethiopia","Ireland","Honduras",
        "Sri Lanka","Bahrain","Slovenia","Moldova","Armenia","Qatar",
        "Cuba","Bosnia and Herzegovina","Libya","Kenya","Myanmar","Zambia",
        "Nigeria","S. Korea","North Macedonia","Algeria","Latvia","Kyrgyzstan",
        "Norway","Albania","Mongolia","Estonia","Afghanistan","Uzbekistan",
        "Montenegro","Namibia","Finland","Ghana","Uganda","Mozambique",
        "Cameroon","Cyprus","El Salvador","Maldives","Botswana","Luxembourg",
        "Singapore","Zimbabwe","Cambodia","Jamaica","Ivory Coast","Rwanda",
        "Senegal","DRC","Madagascar","Angola","Malawi","Sudan",
        "Trinidad and Tobago","Cabo Verde","Réunion","Australia","Malta","French Guiana",
        "Syria","Gabon","Guinea","Vietnam","Suriname","Mauritania",
        "Guyana","Eswatini","Mayotte","Haiti","French Polynesia","Papua New Guinea",
        "Guadeloupe","Seychelles","Taiwan","Somalia","Mali","Togo",
        "Andorra","Tajikistan","Burkina Faso","Belize","Bahamas","Congo",
        "Martinique","Curaçao","Hong Kong","Lesotho","Djibouti","Aruba",
        "South Sudan","Timor-Leste","Equatorial Guinea","Nicaragua","Benin","Fiji",
        "CAR","Yemen","Iceland","Eritrea","Gambia","Sierra Leone",
        "Burundi","Niger","Saint Lucia","San Marino","Liberia","Chad",
        "Channel Islands","Gibraltar","Barbados","Comoros","Guinea-Bissau","Liechtenstein",
        "New Zealand","Sint Maarten","Monaco","Bermuda","Laos","Turks and Caicos",
        "Sao Tome and Principe","Saint Martin","Bhutan","St. Vincent Grenadines","Mauritius","Caribbean Netherlands",
        "Isle of Man","Antigua and Barbuda","St. Barth","Faeroe Islands","British Virgin Islands","Diamond Princess",
        "Cayman Islands","Saint Kitts and Nevis","Tanzania","Wallis and Futuna","Brunei","Dominica",
        "Grenada","New Caledonia","Anguilla","Falkland Islands","Macao","Greenland",
        "Vatican City","Saint Pierre Miquelon","Montserrat","Solomon Islands","Western Sahara","MS Zaandam",
        "Vanuatu","Marshall Islands","Samoa","Saint Helena","Micronesia","China")
         
        self.combo.current(1) 
        self.combo.place(x=350,y=550)
        tk.Label(self,text="Total Cases in",font=("Impact",10),fg="white",bg="#010E1E").place(x=200,y=550)
        tk.Button(self,text="Search",command=self.choose_country, borderwidth = 0).place(x=500,y=550)


        
        self.nickname = txt_user
        self.password = txt_pass
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop) 
        receive_thread = threading.Thread(target = self.receive)
        gui_thread.start()
        receive_thread.start()
        self.pack(fill="both", expand=True)
        self.mainloop()

    
    def gui_loop(self):
    

        self.text_area = tk.scrolledtext.ScrolledText(self)
        self.text_area.place(x=200, y=5)
        self.text_area.config(state='disabled',fg="#00B7FE")
        self.text_area.configure(bg="white")
    
        tk.Label(self,image=self.chat_msg,bg="#010E1E").place(x=500,y=400)

        self.input_area = tk.Text(self, height=3)
        self.input_area.config(font=("Transformers Movie",10))
        self.input_area.place(x=200, y=470)

 
        
        self.send_label.place(x=800,y=470)
        self.out_label.place(x=1000,y=30)
  
# Create def of button and set image
        

        self.gui_done = True

        # self.parent.protocol("WM_DELETE_WINDOW", self.stop)

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
    def User_manual(self):
        manual=Tk()
        manual.resizable(False,False)
        manual.geometry("400x400")
        self.text_user = tk.scrolledtext.ScrolledText(manual)
        self.text_user.config(state='disabled',fg="#00B7FE")
        self.text_user.configure(bg="white")
        self.text_user.place(x=0,y=0,width=400,height=400)
    def choose_country(self):
        self.country=self.combo.get()
        Country=self.country
        self.country="/covid "+self.country
        name_country = f"{self.nickname} : {self.country}\n"
        self.sock.send(name_country.encode('utf-8'))

        self.text_area.config(state='normal')
        self.text_area.insert('end', f"server: You find covid-19 at {Country}. Half a moment \n") 
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

        

#-------------------------------------------------------------------------------
    def write(self,event=None):
        if(self.input_area.get('1.0', 'end') != '\n' ):
            message = f"{self.nickname} : {self.input_area.get('1.0', 'end')}"
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
                if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                print("you disconnected ...")
                
                self.sock.close()
                break
            except ConnectionResetError:
                messagebox.showinfo(title='No Connection !', message="Server offline..try connecting again later")
                self.sock.close()
                self.first_screen()
                break 
    def first_screen(self):
        self.destroy()
        self.parent.geometry("1000x600")
        self.parent.first_frame.pack(fill="both", expand=True)
        self.window = None
    def on_closing(self):
        if self.window == 'ChatScreen':
            res = messagebox.askyesno(title='Warning !',message="Do you really want to disconnect ?")
            if res:
                print("ABCDEF")
                self.sock.close()
                self.first_screen()
        else:
            self.parent.destroy()



FirstScreen()