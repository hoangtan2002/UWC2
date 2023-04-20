titleList = ["Quet rac", "Thu rac", "Lai xe"]

class employeeAtribute():
    name = ""
    age = 0
    title = ""
    def __init__(self,name,age,title):
        self.name = name
        self.age = age
        self.title = title
    
class employeeManager():
    employeeList = []
    employeeAtributeList = []
    employeeCount = 0
    def __init__(self):
        self.add("A",30,"Quet rac")
        self.add("B",25,"Lai xe")
        self.add("C",37,"Don rac")
        print(self.employeeAtributeList)
    def add(self,name,age,title):
        self.employeeList.append(name)
        self.employeeAtributeList.append(employeeAtribute(name,age,title))
        self.employeeCount+=1
        print(self.employeeAtributeList)
    def edit(self,oldName, name, age, title):
        for i in range(self.employeeCount):
            if self.employeeAtributeList[i].name == oldName:
                self.employeeList[i] == name
                self.employeeAtributeList[i].name = name
                self.employeeAtributeList[i].age = age
                self.employeeAtributeList[i].title = title    
        print(self.employeeAtributeList)          
    def delete(self,name):
        for i in range(self.employeeCount):
            if(self.employeeAtributeList[i].name == name):
                self.employeeAtributeList.pop(i)
                self.employeeList.pop(i)
                break
        self.employeeCount -= 1 
        print(self.employeeAtributeList)
    def getInfo(self, name):
        for i in range(self.employeeCount):
            if self.employeeAtributeList[i].name == name:
                return (self.employeeAtributeList[i].name,
                        self.employeeAtributeList[i].age,
                        self.employeeAtributeList[i].title)
        return ("",0,"")
    def getList(self):
        return self.employeeList
    def getIndex(self,name):
        for i in range(self.employeeCount):
            if self.employeeList[i] == name:
                return i
                break
        return 0
    def __del__(self):
        print("Object killed")