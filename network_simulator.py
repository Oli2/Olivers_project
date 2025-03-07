import tkinter as tk # imports tkinter in order to help us with the production of GUI
from tkinter import simpledialog # imports a subclass of tkinter to help us with pop up dialogs for the users input
import tkinter.font as tkfont
import math

class HardwareWidget: #class made for creation of singular Draggable widget
    def __init__ (self, Screen, x, y, HardwareCount, Label, GuiStart): #constructor initializes a HardwareWidget instance
        self.Screen = Screen # Screen is the Tkinter window
        self.GuiStart = GuiStart # allows communication with the class gui_start
        self.x = x # inital x-axisposition
        self.y = y # initial y-axisposition
        self.Label = Label # Label = the name for the widget e.g "Router 3"
        self.HardwareCount = HardwareCount # a count for the number of each widgets duplications to help with the Label of the widget
        self.Duplicate = False #helps us to see if a widget has been Duplicated and shouldnt be Duplicated again
        #^^^ these are all instance variables which store the initial values for the simulator
        self.widget = tk.Label(Screen, text=Label,font = tk.font.BOLD, bg="red", width = 27, height = 7, borderwidth = 3, relief = "solid")# creates a widget representing a piece of hardware
        #^^^ text = Label of hardware, bg = the background colour, width and height = widgets size, borderwidth and relief = makes the Label look like a button
        self.widget.place(x=x, y=y) #places it in the intial positions of x and y
        self.InputDone = False #makes sure a widget is not asked its parameters again
        self.HardwareList = [] #stores the parameters of the hardware
        self.Draggable = True

        if Label == "Internet":
            self.widget.config(bg="lightgreen")
            self.widget.config(width = 15, height = 5)
            self.Draggable = False# makes sure that the internet is green and cant be Duplicated
        elif self.Label.startswith("Router"):
            self.widget.config(bg="lightblue")
        elif self.Label.startswith("Switch"):
            self.widget.config(bg="lightpink")
        elif self.Label.startswith("PC"):
            self.widget.config(bg="yellow")

        self.widget.bind("<Button-1>", self.Click) #binding the leftmouse button Click too Click
        self.widget.bind("<B1-Motion>", self.Drag) #binding left mouse button Drag too Drag
        self.widget.bind("<ButtonRelease-1>", self.Release) #binfing left mouse button Release to Release
        self.widget.bind("<Button-3>",self.Delete)
        self.widget.bind("<Double-Button-1>", self.SelectConnection)

    def SelectConnection(self, event):
        self.GuiStart.SelectWidget(self)

    def Delete(self,event):
        self.widget.destroy()
        for connection in list(self.GuiStart.connections):
            if connection.Widget1 == self or connection.Widget2 ==self:
                self.GuiStart.canvas.delete(connection.line)
                self.GuiStart.connections.remove(connection)

        for hardware in self.GuiStart.widgets:
            if hardware == self:
                self.GuiStart.widgets.remove(hardware)
                self.GuiStart.HardwareCount -=1

    def Click(self,event): #defintion for Click event
        if self.Draggable:
            self.widget.lift() #moves the widget to the front in case its hiding behind another widget
            self.OffsetX = event.x
            self.OffsetY = event.y

    def Drag(self,event): #moves widget to cursors position
        if self.Draggable:
            NewX = self.widget.winfo_x() + event.x - self.OffsetX #gets the cursor x-position and sutracts it from the window x-position to get the relative x-position to the window
            NewY = self.widget.winfo_y() + event.y - self.OffsetY #gets the cursor y-position and sutracts it from the window y-position to get the relative y-position to the window
            self.widget.place(x=NewX,y=NewY) #move the widget along with the cursors position
            for connection in list(self.GuiStart.connections):
                if connection.Widget1 == self or connection.Widget2 == self:
                    connection.update()
            if not self.Duplicate and NewX <175: #Only Duplicates if past line and hasnt been Duplicated before
                self.Duplicate = True # updates the duplication to true to prevent multiple duplications not prompted by the user
                new_Label = f"{self.Label[:-1]}{self.HardwareCount}" #creates new Label for widget to be able to differentiate seperate widgets from each other
                self.GuiStart.CreateHardware(NewX -12.5 , NewY, self.HardwareCount, new_Label) #calls the definition from the GuiStart class which creates the new hardware widget

    def Release(self,event): # defines what happens when left mouse button Released
        pass # passes it onto to the subclasses which inherit HardwareWidget

class Connection:
    def __init__(self,canvas, Widget1, Widget2): # initializes the connection with the canvas and two widgets to connect
        self.canvas = canvas
        self.Widget1 = Widget1
        self.Widget2 = Widget2
        self.line = None # stores the ID of the line on the canvas
        self.update()

    def update(self):
        x1 = self.Widget1.widget.winfo_x() + self.Widget1.widget.winfo_width() // 2
        y1 = self.Widget1.widget.winfo_y() + self.Widget1.widget.winfo_height() // 2
        x2 = self.Widget2.widget.winfo_x() + self.Widget2.widget.winfo_width() // 2
        y2 = self.Widget2.widget.winfo_y() + self.Widget2.widget.winfo_height() // 2
        if self.line:
            self.canvas.coords(self.line,x1 ,y1, x2, y2)
        else:
            self.line = self.canvas.create_line(x1, y1,x2, y2, fill = "red", width = 10)

class Router(HardwareWidget):
    def Release(self, event):
        if self.Duplicate and not self.InputDone:
            self.Configure()
            self.InputDone = True
    def Configure(self): #Prompts the user to input the values for the router
        RouterPortSpeed = simpledialog.askfloat("PORT SPEEDS", "Enter the port speed (100Mbps-10000Mbps):", parent=self.Screen) #uses the subclass of tkinter we inputted earlier to ask the user for the port speed they would like to set the router too
        NumRouterPorts = simpledialog.askinteger("NO. OF PORTS", "Enter the number of ports (2 ports-8 ports):", parent=self.Screen)#uses the subclass of tkinter we inputted earlier to ask the user for the number of ports they would like to set the router too
        Frequency = simpledialog.askfloat("FREQUENCY", "Enter the frequency (500Mhz -2000Mhz):", parent=self.Screen)#uses the subclass of tkinter we inputted earlier to ask the user for the frequency they would like to set the router too
         # the parent = self.Screen ensure that the dialogs are children of the Screen and therefore appear in front of the gui and not hidden behind
        if RouterPortSpeed is not None and NumRouterPorts is not None and Frequency is not None: #stores all parameters to a list if all inputs are valid
            #self.Label = str("R" + str(self.HardwareCount-1)) #creates a specific list name
            Parameters = [self.Label, RouterPortSpeed, NumRouterPorts, Frequency]
            self.HardwareList.append(Parameters)
            self.GuiStart.StoreHardware(self.HardwareList)
            self.widget.config(text=f"{self.Label}\nPort Speed: {RouterPortSpeed}Mbps\nNumber of Ports: {NumRouterPorts}\n Frequency: {Frequency}Mhz")

class Switch(HardwareWidget):
    def Release(self, event):
        if self.Duplicate and not self.InputDone:
            self.Configure()
            self.InputDone = True
    def Configure(self): #Prompts the user to input the values for the switch
        MaxSwitchBandwidth = simpledialog.askfloat("MAX SWITCH BANDWIDTH", "Enter the maximum bandwidth (10Gbps-16000Gbps): ", parent=self.Screen)
        SwitchSpeed = simpledialog.askfloat("SWITCH SPEED", "Enter the switch speed (1Gbps-100Gbps): ", parent=self.Screen)
        NumSwitchPorts = simpledialog.askinteger("NUMBER OF PORTS", "Enter the number of number of ports (2-20): ", parent = self.Screen)
        SwitchLatency = simpledialog.askfloat("SWITCHING LATENCY", "Enter the switching latency (1µs-10µs):", parent=self.Screen)
        SwitchPortSpeed = simpledialog.askfloat("PORT SPEED", "Enter the port speed (500Mbps-10000Mbps):", parent=self.Screen)
        if MaxSwitchBandwidth is not None and SwitchSpeed is not None and NumSwitchPorts is not None and SwitchLatency is not None and SwitchPortSpeed is not None:
            Parameters = [self.Label, MaxSwitchBandwidth , SwitchSpeed , NumSwitchPorts ,SwitchLatency , SwitchPortSpeed]
            self.HardwareList.append(Parameters)
            self.GuiStart.StoreHardware(self.HardwareList)
            self.widget.config(text=f"{self.Label}\nMax Bandwidth: {MaxSwitchBandwidth}Gbps\nSwitch Speed: {SwitchSpeed}Gbps\nNumber of Ports: {NumSwitchPorts}\nSwitchLatency :{SwitchLatency}µs\n Port Speed: {SwitchPortSpeed}Mbps")

class PC(HardwareWidget):
    def Release(self, event):
        if self.Duplicate and not self.InputDone:
            self.Configure()
            self.InputDone = True
    def Configure(self): #Prompts the user to input the values for the PC
        PacketFetchingActivity = simpledialog.askfloat("ACTIVITY FETCHING", "Enter the bandwidth your PC uses to receive packets from outside the network (1Mbps-50Mbps): ", parent=self.Screen)
        PacketSendingActivity = simpledialog.askfloat("ACTIVITY SENDING", "Enter the bandwidth your PC uses to send packets out of the network (1Mbps-50Mbps): ", parent=self.Screen)
        SpeedCPU = simpledialog.askfloat("CPU SPEED", "Enter the CPU speed (1Ghz-5Ghz):", parent=self.Screen)
        NumPCCores = simpledialog.askinteger("NO. OF CORES", "Enter the number of cores (2-8): ", parent = self.Screen)
        SpeedNIC = simpledialog.askfloat("NIC SPEED", "Enter the NIC speed (100Mbps-10000Mbps):", parent=self.Screen)
        if PacketFetchingActivity is not None and PacketSendingActivity is not None and SpeedCPU is not None and NumPCCores is not None and SpeedNIC is not None:
            Parameters = [self.Label, PacketFetchingActivity, PacketSendingActivity, SpeedCPU, NumPCCores, SpeedNIC]
            self.HardwareList.append(Parameters)
            self.GuiStart.StoreHardware(self.HardwareList)
            self.widget.config(text=f"{self.Label}\nFetching Bwidth: {PacketFetchingActivity}Mbps\nSending Bwidth: {PacketSendingActivity}Mbps\nSpeed of CPU: {SpeedCPU}Ghz\nNumber of Cores: {NumPCCores}\nSpeed of NIC :{SpeedNIC}Mbps")
'''class SimulateNetwork(Router,Switch,PC):
    def CalculateLatency(self):

    def CalculateBandwidthUsage(self):

    def CalculateSpeed(self):'''

class GuiStart: # the main gui class that manages all the widgets and connections
    def __init__(self, width=1200, height=800): # constructor that provides the users gui dimensions
        self.width = width #width in pixels of Screen
        self.height = height #height in pixels of Screen
        self.HardwareCount = 1

        self.Screen = tk.Tk() # creates main application window
        self.Screen.title("Network Simulator") #window title
        self.Screen.geometry(f"{width}x{height}") # windows size taken from constructor

        self.canvas = tk.Canvas(self.Screen, width=width, height=height, bg="grey", bd=0) # creates a white canvas for user
        self.canvas.pack(fill="both") # fills the entire window
        self.canvas.create_line(275, 0, 275, height, fill="black", width=6) # draws a vertical black line to seperate the toolbar from the rest of the Screen
        self.widgets = [] # stores all hardware widgets
        self.SetupHardware() #adds default components
        self.AddInstructionBox()
        self.connections = []
        self.SelectedWidget = None
        self.SimulateButton = tk.Button(self.Screen, text = "SIMULATE",font = tkfont.BOLD, bg="SlateBlue1", width = 19, height = 4, borderwidth = 3, relief = "solid")
        self.SimulateButton.place(x= 1010, y = 705)
    def AddInstructionBox(self):
        text = (
            "Instructions:\n"
            "Drag components from left panel\n"
            "into the right panel.\n"
            "Input the parameters.\n"
            "Right-Click to Delete\n"
            "Double-Click to start connection\n"
            "at widget and double click where\n"
            "you want it to end\n"
            )
        self.instructions = tk.Label(self.Screen, text = text, bg="white", font = tkfont.BOLD, fg= "black", width = 27, height = 19, borderwidth = 2, relief = "solid")
        self.instructions.place(x=15,y=440)

    def SetupHardware(self): # method to create default components
        DefaultWidgets = [(600, 2, 0, "Internet"),(15, 20, 1, "Router 1"),(15, 160, 1, "Switch 1"),(15, 300, 1, "PC 1")]  #list of the x-position, y-position and Label of the default components
        for x, y ,HardwareCount, Label in DefaultWidgets: # loop through all hardware_items and run them through CreateHardware
            self.CreateHardware(x, y ,HardwareCount, Label)

    def CreateHardware(self, x, y, HardwareCount,Label): #definiton to create a new widget
        HardwareCount +=  1
        if Label.startswith("Router"):
            widget = Router(self.Screen,x,y,HardwareCount,Label=Label,GuiStart = self)
        if Label.startswith("Switch"):
            widget = Switch(self.Screen,x,y,HardwareCount,Label=Label,GuiStart = self)
        if Label.startswith("PC"):
            widget = PC(self.Screen,x,y,HardwareCount,Label=Label,GuiStart = self)
        if Label.startswith("Internet"):
            widget = HardwareWidget(self.Screen, x, y, HardwareCount, Label=Label, GuiStart=self)

           #widget = HardwareWidget(self.Screen, x, y, HardwareCount, Label=Label, GuiStart=self) #creates new widget

    def StoreHardware(self,HardwareList):
        self.widgets.append(HardwareList)
        print(self.widgets)

    def SelectWidget(self, widget):
        if not self.SelectedWidget:
            self.SelectedWidget = widget
            widget.widget.config(bg="orange")
        else:
            if self.SelectedWidget != widget:
                self.CreateConnection(self.SelectedWidget, widget)
            self.ResetWidgetColour(self.SelectedWidget)
            self.ResetWidgetColour(widget)
            self.SelectedWidget = None

    def ResetWidgetColour(self, SelectedWidget):
        if self.SelectedWidget.Label.startswith("Router"):
            self.SelectedWidget.widget.config(bg="lightblue")
        if self.SelectedWidget.Label.startswith("Switch"):
            self.SelectedWidget.widget.config(bg="lightpink")
        if self.SelectedWidget.Label.startswith("PC"):
            self.SelectedWidget.widget.config(bg="yellow")
        if self.SelectedWidget.Label.startswith("Internet"):
            self.SelectedWidget.widget.config(bg="lightgreen")

    def CreateConnection(self, Widget1,Widget2):
        connection = Connection(self.canvas, Widget1, Widget2)
        self.connections.append(connection)
        print(f"Connection created: {Widget1.Label} <<-->> {Widget2.Label}")

    def Start(self):
        self.Screen.mainloop()

if __name__ == "__main__":
    gui = GuiStart()
    gui.Start()

#https://www.tcl-lang.org/man/tcl8.4/TkCmd/winfo.htm
#https://www.geeksforgeeks.org/how-to-set-border-of-tkinter-Label-widget/
#https://tkinterexamples.com/events/mouse/
