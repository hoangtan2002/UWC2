import tkinter as tk
from tkinter import messagebox
import socket
import threading
import requests
from requests.auth import HTTPBasicAuth
import sys

window = tk.Tk()
window.title("Sever")

server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8085
client_name = " "
clients = []
clients_names = []

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=45)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

def getServerInfo():
    ADDR="127.0.0.1"
    PORT="8080"
    return (ADDR, PORT)

# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    HOST_ADDR, HOST_PORT= getServerInfo();
    
    if HOST_PORT == "0":
        tk.messagebox.showerror(title="ERROR!!!", message="You must enter an address and a port to start server")
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)
    server.bind((HOST_ADDR, int(HOST_PORT)))
    server.listen(5)  # server is listening for client connection
    threading._start_new_thread(accept_clients, (server, " "))
    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    sys.exit(0)
    
def verifyCred(username, passwd):
    #TODO: Implement a system to check for user's username and password 
    return 0

def writeInfo(username, passwd):
    #TODO: Implement a system to write requestant's usr and pass
    # clientDb = open("./client_info")
    # clientDb.write(username+":"+passwd)
    # clientDb.close()
    return 0

def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clientInfo=client.recv(4096).decode()
        print(clientInfo)
        clientInfoSplited = clientInfo.split(":")
        print(clientInfoSplited[0])
        print(clientInfoSplited[1])
        print(clientInfoSplited[2])
        
        if(clientInfoSplited[0] == "R"):
            err = writeInfo(clientInfoSplited[1], clientInfoSplited[2])
            if(err==1):
                errMsg = "E:Username_already_existed"
                client.send(errMsg.encode())
            else:
                succMsg = "S:Registered_Sucessfully"
                client.send(succMsg.encode())
        if(clientInfoSplited[0] == "L"):
            err = verifyCred(clientInfoSplited[1], clientInfoSplited[2])
            if(err==1):
                errMsg = "E:Username_and_or_password_incorrect"
                client.send(errMsg.encode())
            else:
                succMsg = "S:Login_Sucessfully"
                client.send(succMsg.encode()) 
                clients.append(client)
                threading._start_new_thread(send_receive_client_message, (clientInfoSplited[1], client, addr))
            
# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_name, client_connection, client_ip_addr):
    global server, clients, clients_addr
    client_msg = " "
    print("Server:" + client_name)
    welcome_msg = "Welcome " + client_name + ". Use 'exit' to quit"
    client_connection.send(welcome_msg.encode())
    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display
    while True:
        data = client_connection.recv(4096).decode()
        if not data: break
        if data == "exit": break

        client_msg = data
        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]
        print("Receiverd from " + sending_client_name + ": " + data)
        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()
    update_client_names_display(clients_names)  # update client names display

# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)

start_server()
window. state(newstate='iconic')
window.mainloop()       