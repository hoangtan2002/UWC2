import tkintermapview
import geocoder
import tkinter as tk

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