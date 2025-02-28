import tkinter as tk # imports tkinter in order to help us with the production of GUI
from tkinter import simpledialog # imports a subclass of tkinter to help us with pop up dialogs for the users input

class hardware_widget: #class made for creation of singular draggable widget
    def __init__ (self, screen, x, y, hardware_count, label, gui_instance): #constructor initializes a hardware_widget instance
        self.screen = screen # screen is the Tkinter window
        self.gui_instance = gui_instance # allows communication with the class gui_start
        self.x = x # inital x-axisposition
        self.y = y # initial y-axisposition
        self.label = label # label = the name for the widget e.g "Router 3"
        self.hardware_count = hardware_count # a count for the number of each widgets duplications to help with the label of the widget 
        self.duplicate = False #helps us to see if a widget has been duplicated and shouldnt be duplicated again
        #^^^ these are all instance variables which store the initial values for the simulator
        self.widget = tk.Label(screen, text=label, bg="red", width = 20, height = 7, borderwidth = 5, relief = "solid")# creates a widget representing a piece of hardware
        #^^^ text = label of hardware, bg = the background colour, width and height = widgets size, borderwidth and relief = makes the label look like a button
        self.widget.place(x=x, y=y) #places it in the intial positions of x and y
        
        if label == "Internet":
            self.widget.config(bg="green") # makes sure that the internet is green and cant be duplicated
        
        self.widget.bind("<Button-1>", self.click) #binding the leftmouse button click too click
        self.widget.bind("<B1-Motion>", self.drag) #binding left mouse button drag too drag
        self.widget.bind("<ButtonRelease-1>", self.release) #binfing left mouse button release to release
        
    def click(self,event): #defintion for click event
        self.widget.lift() #moves the widget to the front in case its hiding behind another widget
        self.offset_x = event.x
        self.offset_y = event.y
        
        
    def drag(self,event): #moves widget to cursors position
        new_x = self.widget.winfo_x() + event.x - self.offset_x #gets the cursor x-position and sutracts it from the window x-position to get the relative x-position to the window
        new_y = self.widget.winfo_y() + event.y - self.offset_y #gets the cursor y-position and sutracts it from the window y-position to get the relative y-position to the window
        self.widget.place(x=new_x,y=new_y) #move the widget along with the cursors position
        if not self.duplicate and new_x <175: #Only duplicates if past line and hasnt been duplicated before
            new_label = f"{self.label[:-1]}{self.hardware_count}" #creates new label for widget to be able to differentiate seperate widgets from each other
            self.gui_instance.create_hardware(new_x -12.5 , new_y, self.hardware_count, new_label) #calls the definition from the gui_instance class which creates the new hardware widget
            self.duplicate = True # updates the duplication to true to prevent multiple duplications not prompted by the user
            
    def release(self,event,): # defines what happens when left mouse button released
        if self.duplicate and self.label.startswith("Router"): #if the widget has been duplicated and its label starts with Router then run the configuration of the router
            self.configure_router() #calls the definiton that configures the router
        if self.duplicate and self.label.startswith("Switch"):#if the widget has been duplicated and its label starts with Switch then run the configuration of the switch
            self.configure_switch()#calls the definiton that configures the switch
        if self.duplicate and self.label.startswith("PC"):#if the widget has been duplicated and its label starts with PC then run the configuration of the PC
            self.configure_pc()#calls the definiton that configures the PC
    
    def configure_router(self,): #Prompts the user to input the values for the router
        portspeed = simpledialog.askinteger("PORT SPEEDS", "Enter the port speed:", parent=self.screen) #uses the subclass of tkinter we inputted earlier to ask the user for the port speed they would like to set the router too
        no_ports = simpledialog.askinteger("NO. OF PORTS", "Enter the number of ports:", parent=self.screen)#uses the subclass of tkinter we inputted earlier to ask the user for the number of ports they would like to set the router too
        frequency = simpledialog.askinteger("FREQUENCY", "Enter the frequency:", parent=self.screen)#uses the subclass of tkinter we inputted earlier to ask the user for the frequency they would like to set the router too
         # the parent = self.screen ensure that the dialogs are children of the screen and therefore appear in front of the gui and not hidden behind
        if portspeed and no_ports and frequency: #stores all parameters to a list if all inputs are valid
            self.label = str("Router list " + str(self.hardware_count-1)) #creates a specific list name
            parameters = [self.label, portspeed, no_ports, frequency]
            print(parameters)
    
    def configure_pc(self): #Prompts the user to input the values for the PC
        activity_fetching = simpledialog.askinteger("ACTIVITY FETCHING", "Enter the bandwidth your PC uses to receive packets from outside the network: ", parent=self.screen) 
        activity_sending = simpledialog.askinteger("ACTIVITY SENDING", "Enter the bandwidth your PC uses to send packets out of the network: ", parent=self.screen)
        CPU_speed = simpledialog.askinteger("CPU SPEED", "Enter the CPU speed:", parent=self.screen)
        no_cores = simpledialog.askinteger("NO. OF CORES", "Enter the number of cores: ", parent = self.screen)
        NIC_speed = simpledialog.askinteger("NIC SPEED", "Enter the NIC speed:", parent=self.screen)
        if activity_fetching and activity_sending and CPU_speed and no_cores and NIC_speed:
            self.label = str("PC list " + str(self.hardware_count-1))
            parameters = [self.label, activity_fetching, activity_sending, CPU_speed, no_cores, NIC_speed]
            print(parameters)
            
    #^^^ comment of code is the same as the comments for configure_router just with different vairables
    def configure_switch(self): #Prompts the user to input the values for the switch
        max_bandwidth = simpledialog.askinteger("MAX BANDWIDTH", "Enter the maximum bandwidth: ", parent=self.screen) 
        switch_speed = simpledialog.askinteger("SWITCH SPEED", "Enter the switch speed: ", parent=self.screen)
        no_connections = simpledialog.askinteger("NUMBER OF CONNECTIONS", "Enter the number of connections:", parent=self.screen)
        no_ports = simpledialog.askinteger("NUMBER OF PORTS", "Enter the number of number of ports: ", parent = self.screen)
        switching_latency = simpledialog.askinteger("SWITCHING LATENCY", "Enter the switching latency:", parent=self.screen)
        port_speed = simpledialog.askinteger("PORT SPEED", "Enter the port speed:", parent=self.screen)
        if max_bandwidth and switch_speed and no_connections and no_ports and switching_latency and port_speed:
            self.label = str("Switch list " + str(self.hardware_count-1))
            parameters = [self.label, max_bandwidth , switch_speed ,no_connections , no_ports ,switching_latency , port_speed]
            print(parameters)
    #^^^ comment of code is the same as the comments for configure_router just with different vairables   
    

class GuiStart: # the main gui class that manages all the widgets and connections
    def __init__(self, width=1200, height=800): # constructor that provides the users gui dimensions
        self.width = width #width in pixels of screen
        self.height = height #height in pixels of screen
        self.hardware_count = 1

        self.screen = tk.Tk() # creates main application window
        self.screen.title("Network Simulator") #window title
        self.screen.geometry(f"{width}x{height}") # windows size taken from constructor

        self.canvas = tk.Canvas(self.screen, width=width, height=height, bg="grey", bd=0) # creates a white canvas for user
        self.canvas.pack(fill="both") # fills the entire window
        self.canvas.create_line(175, 0, 175, height, fill="black", width=6) # draws a vertical black line to seperate the toolbar from the rest of the screen
        
        self.widgets = [] # stores all hardware widgets
        self.connections = [] # stores all connections
        self.setup_hardware() #adds default components

    def setup_hardware(self): # defniniton to create default components
        hardware_items = [(600, 2, 0, "Internet"),(15, 20, 1, "Router 1"),(15, 145, 1, "Switch 1"),(15, 270, 1, "PC 1")]  #list of the x-position, y-position and label of the default components
        for x, y ,hardware_count, label in hardware_items: # loop through all hardware_items and run them through create_hardware
            self.create_hardware(x, y ,hardware_count, label)

    def create_hardware(self, x, y, hardware_count, label): #definiton to create a new widget
        hardware_count = hardware_count + 1      
        widget = hardware_widget(self.screen, x, y, hardware_count, label=label, gui_instance=self) #creates new widget
        self.widgets.append(widget) #adds to list of widgets
        
    def start(self):
        self.screen.mainloop()


if __name__ == "__main__":
    gui = GuiStart()
    gui.start()
        
#https://www.tcl-lang.org/man/tcl8.4/TkCmd/winfo.htm
#https://www.geeksforgeeks.org/how-to-set-border-of-tkinter-label-widget/
#https://tkinterexamples.com/events/mouse/
