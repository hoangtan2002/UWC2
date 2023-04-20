loactionList = ["duong Ly Thuong Kiet",
                "duong To Hien Thanh",
                "duong Hoa Hao"]

class taskAtribute():
    name = ""
    location = ""
    employee = ""
    deadline = ""
    def __init__(self,name,location,employee,deadline):
        self.name = name
        self.location = location
        self.employee = employee
        self.deadline = deadline
    
class taskController():
    taskList = []
    taskAtributeList = []
    taskCount = 0
    def __init__(self):
        self.add("Task 1",loactionList[0],"A","18/4/2023")
        self.add("Task 2",loactionList[1],"B","19/4/2023")
        self.add("Task 3",loactionList[2],"C","20/4/2023")
        self.add("Task 4",loactionList[1],"A","15/4/2023")
        print
    def add(self,name,location,employee,deadline):
        self.taskList.append(name)
        self.taskAtributeList.append(taskAtribute(name,location,employee,deadline))
        self.taskCount+=1
        print(self.taskAtributeList)
    def edit(self,oldName,name,location,employee,deadline):
        for i in range(self.taskCount):
            if self.taskAtributeList[i].name == oldName:
               self.taskAtributeList[i].name = name
               self.taskAtributeList[i].location = location
               self.taskAtributeList[i].employee = employee
               self.taskAtributeList[i].deadline = deadline
        print(self.taskAtributeList)
    def delete(self,name):
        for i in range(self.taskCount):
            if self.taskAtributeList[i].name == name:
               self.taskAtributeList.pop(i)
               self.taskList.pop(i)
               self.taskCount-=1
               break
        print(self.taskAtributeList)
    def getList(self):
        return self.taskList
    def getIndex(self,name):
        for i in range(self.taskCount):
            if self.taskAtributeList[i].name == name:
                return i
        return 0
    def getInfo(self, name):
        for i in range(self.taskCount):
            if self.taskAtributeList[i].name == name:
                return (self.taskAtributeList[i].name,
                        self.taskAtributeList[i].location,
                        self.taskAtributeList[i].employee,
                        self.taskAtributeList[i].deadline)
                break
        return ("","","","")
    