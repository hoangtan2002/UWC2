import tkinter as tk                
from tkinter import font as tkfont  
from employeeController import *
from taskController import *
import tkintermapview
import geocoder
import socket
import threading

employeeList = employeeManager()
taskList = taskController()
username="Admin"
password="Admin"

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Roboto', size=18, weight="bold")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, employeeFrame, TaskFrame, mapFrame, chatFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login Page", font=controller.title_font)
        label.pack(side=tk.TOP, anchor=tk.CENTER, expand=tk.YES)
        #Username field
        nameFrame=tk.Frame(self)
        
        lblName = tk.Label(nameFrame, text = "Username:")
        lblName.pack(side=tk.LEFT,expand=tk.YES)
        
        userNameEntry = tk.Entry(nameFrame)
        userNameEntry.pack(side=tk.RIGHT, anchor=tk.CENTER,expand=tk.YES)
        
        nameFrame.pack(side=tk.TOP)
        #Password Field
        passFrame=tk.Frame(self)
        
        lblPass = tk.Label(passFrame, text = "Password:")
        lblPass.pack(side=tk.LEFT)
        
        entPass = tk.Entry(passFrame, show="*")
        entPass.pack(side=tk.RIGHT,anchor=tk.CENTER,expand=tk.YES)
        
        passFrame.pack(side=tk.TOP)
        #Buttons
        loginBtnFrame = tk.Frame(self)
        button1 = tk.Button(loginBtnFrame, text="Login",width=10,
                            command=lambda: controller.show_frame("employeeFrame"))
        button1.pack(side=tk.LEFT)
        button2 = tk.Button(loginBtnFrame, text="Exit",width=10,
                            command=lambda: controller.show_frame("TaskFrame"))
        button2.pack(side=tk.RIGHT)
        loginBtnFrame.pack(side=tk.BOTTOM)


class employeeFrame(tk.Frame):
    
    employeeInfoString = "Select an employee"
    selectedEmployee = ""
    def __init__(self, parent, controller):
        global employeeInfoLabel,employeeListBox
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Employee List", font=controller.title_font)
        label.pack(side=tk.TOP, anchor=tk.CENTER)

        topUiFrame = tk.Frame(self)
        #Side Button
        sideButtonFrame=tk.Frame(topUiFrame)
        
        addButton=tk.Button(sideButtonFrame,width=10,text="Add",
                            command = lambda:self.addEmployeeButton(parent))
        addButton.pack(side=tk.TOP,expand=tk.YES)
        
        editButton=tk.Button(sideButtonFrame,width=10,text="Edit",
                             command=lambda:self.editEmployeeButton(parent))
        editButton.pack(side=tk.TOP,expand=tk.YES)
        
        delButton = tk.Button(sideButtonFrame,width=10,text="Delete",
                              command=lambda:self.deleteEmployee(self.selectedEmployee))
        delButton.pack(side=tk.TOP,expand=tk.YES)
        
        sideButtonFrame.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        #employee list
        employeeListFrame = tk.Frame(topUiFrame)
        employeeListBox = tk.Listbox(employeeListFrame,height = 20,width = 50)
        for i in range(len(employeeList.employeeList)):
            employeeListBox.insert(i+1, employeeList.employeeList[i])
        employeeListBox.bind("<<ListboxSelect>>",self.selectCallback)
        employeeListBox.pack(side=tk.LEFT)
        employeeListFrame.pack(side=tk.LEFT)
        #employee info frame
        employeeInfo = tk.Frame(topUiFrame)
        
        employeeInfoLabel = tk.Label(employeeInfo,text=self.employeeInfoString)
        employeeInfoLabel.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.CENTER)
        employeeInfo.pack(side=tk.RIGHT)  
        
        topUiFrame.pack(side=tk.TOP)
        
        #bottom button frame  
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
        
    def addEmployeeButton(self, parent):
        global addDialog
        addDialog = tk.Toplevel(parent)
        addDialog.title("Add Employee")
        
        #Label frame
        diaglogLabelFrame = tk.Frame(addDialog)
        dialogLabel = tk.Label(diaglogLabelFrame, text="Add Employee")
        dialogLabel.pack(side=tk.TOP, anchor=tk.CENTER)
        diaglogLabelFrame.pack(side=tk.TOP)
        
        #Entry Field
        fieldEntryFrame = tk.Frame(addDialog)
        
        #Name Entry
        nameEntryFrame = tk.Frame(fieldEntryFrame)
        
        nameEntryLabel = tk.Label(nameEntryFrame, text = "Name:")
        nameEntryLabel.pack(side=tk.LEFT)
        
        nameEntry = tk.Entry(nameEntryFrame,width=25)
        nameEntry.pack(side=tk.RIGHT)

        nameEntryFrame.pack(side=tk.TOP)
        
        #Age entry frame
        AgeEntryFrame = tk.Frame(fieldEntryFrame)
        
        AgeEntryLabel = tk.Label(AgeEntryFrame, text = "    Age:")
        AgeEntryLabel.pack(side=tk.LEFT)
        
        AgeEntry = tk.Entry(AgeEntryFrame,width=25)
        AgeEntry.pack(side=tk.RIGHT)

        AgeEntryFrame.pack(side=tk.TOP)
        
        titleSelectionFrame = tk.Frame(fieldEntryFrame)
        
        titleLabel = tk.Label(titleSelectionFrame, text = "Title:")
        titleLabel.pack(side=tk.LEFT)
        
        titleVar = tk.StringVar()
        titleVar.set("******************")
        titleSelection = tk.OptionMenu(titleSelectionFrame,titleVar,*titleList)
        titleSelection.pack(side=tk.RIGHT)
        
        titleSelectionFrame.pack(side=tk.TOP)
        #button Frame
        buttonFrame = tk.Frame(addDialog)
        
        addButton = tk.Button(buttonFrame,width=10,text="Add",
                              command = lambda:self.addEmployeeToList(nameEntry.get().strip(),
                                                                      int(AgeEntry.get().strip()),
                                                                      titleVar.get()))
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        addButton = tk.Button(buttonFrame,width=10,text="Cancel",
                              command = lambda:self.cancelAction())
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        buttonFrame.pack(side=tk.BOTTOM)
        
        fieldEntryFrame.pack(side=tk.TOP)
        
    def editEmployeeButton(self, parent):
        global editDialog
        editDialog = tk.Toplevel(parent)
        editDialog.title("edit Employee")
        
        #Label frame
        diaglogLabelFrame = tk.Frame(editDialog)
        dialogLabel = tk.Label(diaglogLabelFrame, text="edit Employee")
        dialogLabel.pack(side=tk.TOP, anchor=tk.CENTER)
        diaglogLabelFrame.pack(side=tk.TOP)
        
        #Entry Field
        fieldEntryFrame = tk.Frame(editDialog)
        
        #Name Entry
        nameEntryFrame = tk.Frame(fieldEntryFrame)
        
        nameEntryLabel = tk.Label(nameEntryFrame, text = "Name:")
        nameEntryLabel.pack(side=tk.LEFT)
        
        nameEntry = tk.Entry(nameEntryFrame,width=25)
        nameEntry.pack(side=tk.RIGHT)

        nameEntryFrame.pack(side=tk.TOP)
        
        #Age entry frame
        AgeEntryFrame = tk.Frame(fieldEntryFrame)
        
        AgeEntryLabel = tk.Label(AgeEntryFrame, text = "    Age:")
        AgeEntryLabel.pack(side=tk.LEFT)
        
        AgeEntry = tk.Entry(AgeEntryFrame,width=25)
        AgeEntry.pack(side=tk.RIGHT)

        AgeEntryFrame.pack(side=tk.TOP)
        
        titleSelectionFrame = tk.Frame(fieldEntryFrame)
        
        titleLabel = tk.Label(titleSelectionFrame, text = "Title:")
        titleLabel.pack(side=tk.LEFT)
        
        titleVar = tk.StringVar()
        titleVar.set("******************")
        titleSelection = tk.OptionMenu(titleSelectionFrame,titleVar,*titleList)
        titleSelection.pack(side=tk.RIGHT)
        
        titleSelectionFrame.pack(side=tk.TOP)
        #button Frame
        buttonFrame = tk.Frame(editDialog)
        
        editButton = tk.Button(buttonFrame,width=10,text="edit",
                              command=lambda:self.editEmployeeInList(self.selectedEmployee, nameEntry.get().strip(),
                                                                      int(AgeEntry.get().strip()),
                                                                      titleVar.get()))
        editButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        editButton = tk.Button(buttonFrame,width=10,text="Cancel",
                              command = lambda:self.cancelEdit())
        editButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        buttonFrame.pack(side=tk.BOTTOM)
        
        fieldEntryFrame.pack(side=tk.TOP)
        
    def cancelAction(self):
        addDialog.destroy()
    
    def cancelEdit(self):
        editDialog.destroy()
        
    def addEmployeeToList(self,name,age,entry):
        employeeList.add(name,age,entry)
        employeeListBox.insert(employeeList.employeeCount,name)
        print("added an employee")
        addDialog.destroy()
        
    def deleteEmployee(self,name):
        employeeListBox.delete(employeeList.getIndex(name),employeeList.getIndex(name))
        employeeList.delete(name)
        self.selectedEmployee = ""
        employeeInfoLabel["text"] = "Select an amployee"
        
    def editEmployeeInList(self,oldName,newName,age,title):
        oldIndex = employeeList.getIndex(self.selectedEmployee)
        print(oldIndex)
        employeeList.edit(oldName,newName,age,title)
        employeeListBox.delete(oldIndex,oldIndex)
        employeeListBox.insert(oldIndex,newName)
        editDialog.destroy()
        
    def selectCallback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            name,age,title = employeeList.getInfo(event.widget.get(index))
            self.selectedEmployee = name
            employeeInfoLabel["text"] = "Name:" + name + '\n' + "Age:" + str(age) + '\n' + 'Title:' + title 
        else:
            employeeInfoLabel["text"] = "Select an employee"

class TaskFrame(tk.Frame):
    selectedTask = ""
    def __init__(self, parent, controller):
        global taskListBox,taskInfoLabel
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Task List", font=controller.title_font)
        label.pack(side=tk.TOP, anchor=tk.CENTER)

        topUiFrame = tk.Frame(self)
        #Side Button
        sideButtonFrame=tk.Frame(topUiFrame)
        
        addButton=tk.Button(sideButtonFrame,width=10,text="Add",
                            command=lambda:self.addTaskButton(parent))
        addButton.pack(side=tk.TOP,expand=tk.YES)
         
        editButton=tk.Button(sideButtonFrame,width=10,text="Edit",
                             command=lambda:self.editTaskButton(parent))
        editButton.pack(side=tk.TOP,expand=tk.YES)
        
        delButton = tk.Button(sideButtonFrame,width=10,text="Delete",
                              command=lambda:self.deleteTaskFromList(self.selectedTask))
        delButton.pack(side=tk.TOP,expand=tk.YES)
        
        sideButtonFrame.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        #task list
        taskListFrame = tk.Frame(topUiFrame)
        taskListBox = tk.Listbox(taskListFrame,height = 20,width = 50)
        for i in range(len(taskList.taskList)):
            taskListBox.insert(i+1, taskList.taskList[i])
        taskListBox.pack(side=tk.LEFT, anchor=tk.CENTER)
        taskListBox.bind("<<ListboxSelect>>",self.selectCallback)
        taskListFrame.pack(side=tk.LEFT)

        #task info frame
        taskInfo = tk.Frame(topUiFrame)
        taskInfoLabel = tk.Label(taskInfo,text="Select a Task")
        taskInfoLabel.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.CENTER)
        taskInfo.pack(side=tk.LEFT)  
        
        topUiFrame.pack(side=tk.TOP)
        #bottom button frame  
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
        
    def addTaskButton(self,parent):
        global addDialog
        addDialog = tk.Toplevel(parent)
        addDialog.title("Add Employee")
        
        #Label frame
        diaglogLabelFrame = tk.Frame(addDialog)
        dialogLabel = tk.Label(diaglogLabelFrame, text="Add Task")
        dialogLabel.pack(side=tk.TOP, anchor=tk.CENTER)
        diaglogLabelFrame.pack(side=tk.TOP)
        
        #Entry Field
        fieldEntryFrame = tk.Frame(addDialog)
        
        #Name Entry
        nameEntryFrame = tk.Frame(fieldEntryFrame)
        
        nameEntryLabel = tk.Label(nameEntryFrame, text = "Name:")
        nameEntryLabel.pack(side=tk.LEFT)
        
        nameEntry = tk.Entry(nameEntryFrame,width=25)
        nameEntry.pack(side=tk.LEFT)

        nameEntryFrame.pack(side=tk.TOP)
        
        #Location Entry
        locationSelectionFrame = tk.Frame(fieldEntryFrame)
        
        locationLabel = tk.Label(locationSelectionFrame, text = "Location:")
        locationLabel.pack(side=tk.LEFT)
        
        locationVar = tk.StringVar()
        locationVar.set("******************")
        locationSelection = tk.OptionMenu(locationSelectionFrame,
                                          locationVar,
                                          *loactionList)
        locationSelection.pack(side=tk.RIGHT)
        
        locationSelectionFrame.pack(side=tk.TOP)
        #Employee Selection
        employeeSelectionFrame = tk.Frame(fieldEntryFrame)
        
        employeeLabel = tk.Label(employeeSelectionFrame, text = "Employee:")
        employeeLabel.pack(side=tk.LEFT)
        
        employeeVar = tk.StringVar()
        employeeVar.set("******************")
        employeeSelection = tk.OptionMenu(employeeSelectionFrame,
                                          employeeVar,
                                          *employeeList.employeeList)
        employeeSelection.pack(side=tk.LEFT)
        
        employeeSelectionFrame.pack(side=tk.TOP)
        
        deadlineEntryFrame = tk.Frame(fieldEntryFrame)
        
        deadlineEntryLabel = tk.Label(deadlineEntryFrame, text = "Deadline:")
        deadlineEntryLabel.pack(side=tk.LEFT)
        
        deadlineEntry = tk.Entry(deadlineEntryFrame,width=25)
        deadlineEntry.pack(side=tk.RIGHT)

        deadlineEntryFrame.pack(side=tk.TOP)
        
        fieldEntryFrame.pack(side=tk.TOP)
            
        #button Frame
        buttonFrame = tk.Frame(addDialog)
        
        addButton = tk.Button(buttonFrame,width=10,text="Add",
                              command=lambda:self.addTaskToList(
                                  nameEntry.get().strip(),
                                  locationVar.get(),
                                  employeeVar.get(),
                                  deadlineEntry.get()
                       ))
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER,)
        
        addButton = tk.Button(buttonFrame,width=10,text="Cancel",
                              command = lambda:self.cancelAction())
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        buttonFrame.pack(side=tk.BOTTOM)
        
    def editTaskButton(self,parent):
        global editDialog
        editDialog = tk.Toplevel(parent)
        editDialog.title("Edit Employee")
        
        #Label frame
        diaglogLabelFrame = tk.Frame(editDialog)
        dialogLabel = tk.Label(diaglogLabelFrame, text="Edit Task")
        dialogLabel.pack(side=tk.TOP, anchor=tk.CENTER)
        diaglogLabelFrame.pack(side=tk.TOP)
        
        #Entry Field
        fieldEntryFrame = tk.Frame(editDialog)
        
        #Name Entry
        nameEntryFrame = tk.Frame(fieldEntryFrame)
        
        nameEntryLabel = tk.Label(nameEntryFrame, text = "Name:")
        nameEntryLabel.pack(side=tk.LEFT)
        
        nameEntry = tk.Entry(nameEntryFrame,width=25)
        nameEntry.pack(side=tk.LEFT)

        nameEntryFrame.pack(side=tk.TOP)
        
        #Location Entry
        locationSelectionFrame = tk.Frame(fieldEntryFrame)
        
        locationLabel = tk.Label(locationSelectionFrame, text = "Location:")
        locationLabel.pack(side=tk.LEFT)
        
        locationVar = tk.StringVar()
        locationVar.set("******************")
        locationSelection = tk.OptionMenu(locationSelectionFrame,
                                          locationVar,
                                          *loactionList)
        locationSelection.pack(side=tk.RIGHT)
        
        locationSelectionFrame.pack(side=tk.TOP)
        #Employee Selection
        employeeSelectionFrame = tk.Frame(fieldEntryFrame)
        
        employeeLabel = tk.Label(employeeSelectionFrame, text = "Employee:")
        employeeLabel.pack(side=tk.LEFT)
        
        employeeVar = tk.StringVar()
        employeeVar.set("******************")
        employeeSelection = tk.OptionMenu(employeeSelectionFrame,
                                          employeeVar,
                                          *employeeList.employeeList)
        employeeSelection.pack(side=tk.LEFT)
        
        employeeSelectionFrame.pack(side=tk.TOP)
        
        deadlineEntryFrame = tk.Frame(fieldEntryFrame)
        
        deadlineEntryLabel = tk.Label(deadlineEntryFrame, text = "Deadline:")
        deadlineEntryLabel.pack(side=tk.LEFT)
        
        deadlineEntry = tk.Entry(deadlineEntryFrame,width=25)
        deadlineEntry.pack(side=tk.RIGHT)

        deadlineEntryFrame.pack(side=tk.TOP)
        
        fieldEntryFrame.pack(side=tk.TOP)
            
        #button Frame
        buttonFrame = tk.Frame(editDialog)
        
        addButton = tk.Button(buttonFrame,width=10,text="Ok",
                              command=lambda:self.editTaskInList(
                                  self.selectedTask,
                                  nameEntry.get().strip(),
                                  locationVar.get(),
                                  employeeVar.get(),
                                  deadlineEntry.get()
                       ))
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER,)
        
        addButton = tk.Button(buttonFrame,width=10,text="Cancel",
                              command = lambda:self.cancelAction())
        addButton.pack(side=tk.LEFT,anchor=tk.CENTER)
        
        buttonFrame.pack(side=tk.BOTTOM)
        
    def addTaskToList(self,name,location,employee,deadline):
        taskList.add(name,location,employee,deadline)
        taskListBox.insert(taskList.taskCount,name)
        addDialog.destroy()
        print()
        
    def cancelAction(self):
        addDialog.destroy()
        print()
    
    def deleteTaskFromList(self, name):
        taskListBox.delete(taskList.getIndex(name),taskList.getIndex(name))
        taskList.delete(name)
        taskInfoLabel["text"] = "Select a task"
    
    def selectCallback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            name,location,employee,deadline = taskList.getInfo(event.widget.get(index))
            taskInfoLabel["text"] = "Name:"+name+'\n'+"Location:"+location+"\n"+"Employee assigned:" + employee +"\n" + "Deadline:"+deadline
            self.selectedTask = name
        else:
            taskInfoLabel["text"] = "Select a task"
            
    def editTaskInList(self, oldName, name, location, employee, deadline):
        oldIndex = taskList.getIndex(oldName)
        taskList.edit(oldName,name,location,employee,deadline)
        taskListBox.delete(oldIndex,oldIndex)
        taskListBox.insert(oldIndex,name)
        editDialog.destroy()
        
    def cancelEdit():
        editDialog.destroy()

class mapFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        map_widget = tkintermapview.TkinterMapView(self,width=600,height=450,corner_radius=25)
        map_widget.pack(side=tk.TOP,anchor=tk.CENTER)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        g = geocoder.ip('me')
        try:
            map_widget.set_position(g.latlng[0],g.latlng[1])
        except:
            print("Time out")
        print(g.latlng)
        
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
         
if __name__ == "__main__":
    app = App()
    app.mainloop()
