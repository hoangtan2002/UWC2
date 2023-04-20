import tkinter as tk 
import threading
import socket

username="Admin"
password="Admin"

class chatFrame(tk.Frame):
    global tkDisplay,tkMessage
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        displayFrame = tk.Frame(self)
        lblLine = tk.Label(displayFrame, text="*************************************************************************").pack()
        scrollBar = tk.Scrollbar(displayFrame)
        self.tkDisplay = tk.Text(displayFrame, height=20, width=55)
        self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.tkDisplay.tag_config("tag_your_message", foreground="blue")
        self.tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollBar.config(command=self.tkDisplay.yview)
        displayFrame.pack(side=tk.TOP)

        midFrame = tk.Frame(self)
        self.tkMessage = tk.Text(midFrame, height=2, width=50)
        self.tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(highlightbackground="grey")
        sendBtn = tk.Button(midFrame, text="Send->", command=lambda:self.getChatMessage(self.tkMessage.get("1.0", tk.END)))
        self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(self.tkMessage.get("1.0", tk.END))))
        sendBtn.pack(side=tk.RIGHT)
        midFrame.pack(side=tk.TOP)
        
        bottomFrame=tk.Frame(self)
        HomeBtn=tk.Button(bottomFrame,width=12,text="Home")
        HomeBtn.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        employeeBtn=tk.Button(bottomFrame,width=12,text="Employee",
                              command=lambda:controller.show_frame("employeeFrame"))
        employeeBtn.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        TaskBtn=tk.Button(bottomFrame,width=12,text="Task",
                          command=lambda:controller.show_frame("TaskFrame"))
        TaskBtn.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        mapBtn=tk.Button(bottomFrame,width=12,text="Map",
                         command=lambda:controller.show_frame("mapFrame"))
        mapBtn.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        ChatBtn=tk.Button(bottomFrame,width=12,text="Chat",
                          command=lambda: controller.show_frame("chatFrame"))
        ChatBtn.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        bottomFrame.pack(side=tk.BOTTOM,anchor=tk.CENTER, expand=tk.YES)
        
        self.login()
        
    def getServerInfo(self):
        ADDR="127.0.0.1"
        PORT="8080"
        
        return (ADDR, PORT)

            
    def login(self):
        self.connect_to_server(username,password)
                    
    def connect_to_server(self,name, password):
        global client, HOST_PORT, HOST_ADDR
        try:
            HOST_ADDR, HOST_PORT= self.getServerInfo();
            
            if HOST_PORT == "0":
                tk.messagebox.showerror(title="ERROR!!!", message="You must enter the address and poet of server to connect to")
                return
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST_ADDR, int(HOST_PORT)))
            login_info = "L:" + name + ":" + password;
            client.send(login_info.encode())# Send name to server after connecting
            fromServer = client.recv(4096).decode()
            print(fromServer)
            fromServerSplited = fromServer.split(":")

            if(fromServerSplited[0]=="S"): 
                threading._start_new_thread(self.receive_message_from_server, (client, "m"))
            
            else:
                tk.messagebox.showerror(title="ERROR!!!", message = fromServerSplited[1])
                client.close()
                
        except Exception as e:
            tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

    def receive_message_from_server(self,sck,m):
        while True:
            from_server = sck.recv(4096).decode()

            if not from_server: break

            # display message from server on the chat window
            # enable the display area and insert the text and then disable.
            # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
            texts = self.tkDisplay.get("1.0", tk.END).strip()
            self.tkDisplay.config(state=tk.NORMAL)
            
            if len(texts) < 1:
                self.tkDisplay.insert(tk.END, from_server)
            else:
                self.tkDisplay.insert(tk.END, "\n\n"+ from_server)

            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)

            # print("Server says: " +from_server)

        sck.close()

    def getChatMessage(self,msg):

        msg = msg.replace('\n', '')
        texts = self.tkDisplay.get("1.0", tk.END).strip()

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
        self.tkDisplay.config(state=tk.NORMAL)
        
        if len(texts) < 1:
            self.tkDisplay.insert(tk.END, "You->" + msg , "tag_your_message") # no line
        else:
            self.tkDisplay.insert(tk.END, "\n\n" + "You->" + msg , "tag_your_message")

        self.tkDisplay.config(state=tk.DISABLED)

        self.send_mssage_to_server(msg)

        self.tkDisplay.see(tk.END)
        self.tkMessage.delete('1.0', tk.END)


    def send_mssage_to_server(self,msg):
        client_msg = str(msg)
        client.send(client_msg.encode())
        
        if msg == "exit":
            client.close()
        print("Sending message")