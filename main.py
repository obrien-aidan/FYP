#-----------IMPORTS-----------
import cv2
from cv2 import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image as Img
from PIL import ImageTk
import serial
import time
from serial import Serial
import serial
import time
import numpy as np
from tkinter import ttk,messagebox
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import serial.tools.list_ports
from PIL import Image
import PIL
import sqlite3
import time
import datetime
from pathlib import Path
#----------- / IMPORTS-----------


#-----------PORT SETUP-----------
#set robot serial port
robotSer = serial.Serial("COM13", 250000)
#delay for 3D printer initilization 
time.sleep(5)
#home axis
robotSer.write(b'G28 X Y Z\n')
#wait for axis to home
time.sleep(5)
#set movement to absolute
robotSer.write(b'G90\n')
#wait to ensure absolute setting is transmitted
time.sleep(2)
#set the z axis to be 15 from top
robotSer.write(b'G0 Z15\n')
#set the led analyser serial port
laSer = serial.Serial("COM9", 57600)
#set the power supply serial port
ser2 = serial.Serial("COM5", 9600)
# starting camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #camera port 0
#setting the exposure value
cap.set(cv2.CAP_PROP_EXPOSURE, -5.5)
#----------- / PORT SETUP-----------


#-----------SPLASH------------------
def splash():
    #new window
    splash=Tk()
    #color variable
    a='white'
    #window icon location
    splash.iconbitmap(Path(__file__).parent / "images/logo_R8v_icon.ico")
    #setting the title of the splash window
    splash.title('Welcome')
    #setting the background
    splash.config(bg=a)
    #set to not be resizable
    splash.resizable(False,False)
    #set the window height
    window_height = 400
    #set the window width
    window_width = 450
    #getting screen information to centre the splash screen
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    #centering the splash screen
    splash.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    #first logo path
    logos=Image.open(Path(__file__).parent / "images/witlogo.jpg")
    #resizing the logo
    resized_l = logos.resize((140,150),Image.ANTIALIAS)
    #format as image
    logo1 = ImageTk.PhotoImage(resized_l)
    #setting as label to place in grid
    logo = Label(splash, image=logo1, bd=0)
    #placing in the grid
    logo.grid(row=0,column=0,padx=(70,10),pady=(40,20))
    #second logo path
    logos2=Image.open(Path(__file__).parent / "images/feasalogo.jpg")
    #resizing the logo
    resized_l2 = logos2.resize((140,150),Image.ANTIALIAS)
    #format as image
    logo2 = ImageTk.PhotoImage(resized_l2)
    #setting as label to place in grid
    logo3 = Label(splash, image=logo2, bd=0)
    #placing in the grid
    logo3.grid(row=0,column=1,padx=(10,70),pady=(40,20))
    #text1
    l1=Label(splash,text='Vision-Based Robotic System',fg="#00adb5",bg=a,font=('HELVETICA',18,'bold'))
    #placing text on grid
    l1.grid(row=1,column=0,padx=10,pady=(20,10),columnspan=2)
    #text2
    l2=Label(splash,text='for light metrology',fg='#393e46',bg=a,font=('HELVETICA',14))
    #placing text on grid
    l2.grid(row=2,column=0,padx=10,pady=(10,30),columnspan=2)
    #text3
    l3=Label(splash,text="AidanO'Brien 2021",fg='#393e46',bg=a,font=('HELVETICA',10,'italic'))
    #placing text on grid
    l3.grid(row=3,column=0,padx=10,pady=(10,30),columnspan=2)
    #display for 6 seconds
    splash.after(6000, lambda: splash.destroy())
    splash.mainloop()
#call the splash screen function
splash()
#-----------/ SPLASH------------------


#-----------DB SETUP-----------
#connect
conn = sqlite3.connect('FYP.db')
#cursor absraction
c = conn.cursor()
#turn ON foreign key consraint
c.execute("PRAGMA foreign_keys = ON")
#create the project table
c.execute("CREATE TABLE IF NOT EXISTS project(project_id INTEGER PRIMARY KEY AUTOINCREMENT, datestamp TEXT, numMeasurements INTEGER)")
#time stamp
unix = int(time.time())
#datestamp
datestamp = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
#initalize number of measurements variable
numMeasurements = int(0)
#insert values into table
c.execute("INSERT INTO project(datestamp, numMeasurements ) VALUES (?, ?)",
        (datestamp, numMeasurements))
#create project id variable for measurement table
projectId=c.lastrowid
#commit to save changes
conn.commit()
#----------- / DB SETUP-----------


#-----------WINDOW/FRAME SETUP-----------
#####-------MAIN WINDOW-------#####
# Window
#color setup1
white = "#ffffff"
#color setup2
lightBlue2 = "#393e46"
#font setup
font = "Helvetica"
#font2 setup
fontButtons = (font, 12)
#main window setup
mainWindow = tk.Tk()
#setting the window logo
mainWindow.iconbitmap(Path(__file__).parent / "images/logo_R8v_icon.ico")
#setting the window title
mainWindow.title(' AOB FYP | Vision-Based Robotic System')
#configure background color
mainWindow.configure(bg=lightBlue2)
#matching the window size to the screen size
w = mainWindow.winfo_screenwidth()
h = mainWindow.winfo_screenheight() - 10
mainWindow.geometry("%dx%d+0+0" % (w, h))
#about menu drop down
def showAbout():
        #open window
        about=Toplevel(mainWindow)
        #set the window icon
        about.iconbitmap(Path(__file__).parent / "images/logo_R8v_icon.ico")
        #set the window title
        about.title('About')
        #set the window color
        about.config(bg="white")
        #make non resizable
        about.resizable(False,False)
        #set the window height
        window_height = 225
        #set the window width
        window_width = 225
        #center the window
        screen_width = about.winfo_screenwidth()
        screen_height = about.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        about.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        #adding text and placing on grid
        l1=Label(about,text='Vision-Based Robotic System',fg="#00adb5",bg=white,font=('HELVETICA',10,'bold'))
        l1.grid(row=1,column=0,padx=0,pady=(10,5),columnspan = 2,sticky="ew")
        l2=Label(about,text='for light metrology',fg='#393e46',bg=white,font=('HELVETICA',10))
        l2.grid(row=2,column=0,padx=0,pady=(5,5),sticky="ew")
        l3=Label(about,text='Visit:',fg='#393e46',bg=white,font=('HELVETICA',8))
        l3.grid(row=4,column=0,padx=0,pady=(0,0),sticky="ew")
        l4=Label(about,text='https://linktr.ee/AidanOBrien_FYP',fg='#393e46',bg=white,font=('HELVETICA',8))
        l4.grid(row=5,column=0,padx=0,pady=(0,0),sticky="ew")
        l5=Label(about,text='for more information',fg='#393e46',bg=white,font=('HELVETICA',8))
        l5.grid(row=6,column=0,padx=0,pady=(0,0),sticky="ew")

#setting up menu bar
menu = Menu(mainWindow)
#config as menu
mainWindow.config(menu=menu)
#file drop downdown menu
fileMenu = Menu(menu, tearoff=False, background='#aad8d3')
menu.add_cascade(label='File',menu=fileMenu)
#add seperator before exit
fileMenu.add_separator()
#option for closing the program
fileMenu.add_command(label="Exit",command=mainWindow.destroy)
#setting up help menu
helpMenu = Menu(menu, tearoff=False, background='#aad8d3')
menu.add_cascade(label='Help',menu=helpMenu)
#add a seperator
helpMenu.add_separator()
#open the About window
helpMenu.add_command(label="About",command=lambda: showAbout())
#creating the toolbar
toolbar = Frame(mainWindow, background="#eeeeee")
#places at top of window and fills horizontally
toolbar.pack(side=TOP, fill=X)
#run button image import
run_btn = PhotoImage(file=Path(__file__).parent / "images/play.png")
#formating the image
small = run_btn.subsample(35,35)
#creating the run button - calls the itterateCallback() function
runButt = Button(toolbar, command=lambda :itterateCallBack(), image=small, highlightthickness = 0, bd = 0, state="disabled")
#packing the run button
runButt.pack(side=LEFT, padx=15, pady=10)
#save button image import
save_btn = PhotoImage(file=Path(__file__).parent / "images/save.png")
#formating the image
small1 = save_btn.subsample(35,35)
#creating the save button - calls the saveButton() function
saveButt = Button(toolbar, command=lambda :saveButton(), image=small1, highlightthickness = 0, bd = 0, state="disabled")
#packing the save button
saveButt.pack(side=LEFT, padx=15, pady=10)
#####-------/ MAIN WINDOW-------#####
#####-------VIDEO FRAME-------#####
#creating Frame for video
mainFrame = Frame(mainWindow, bg=lightBlue2)
#packing video frame
mainFrame.pack(side=TOP, anchor=CENTER, fill='x')
#cursor to crosshair 
lmain = tk.Label(mainFrame, cursor='crosshair')
#pack the label 
lmain.pack(side=LEFT, anchor=CENTER, padx=5, pady=5)
#####-------/VIDEO FRAME-------#####

#####-------INPUT FRAME-------#####
#set index to global
global index
#initilaze the index
index = 0
#number column  
a_list = []
#list that contain all the X entries
Entry1_list = []
#list that contain all the Y entries
Entry2_list = []
#list that contain all the combo-box/capture selection
combobox_list = []  
#list that contain all the Voltage entries
Entry3_list = []  
#list that contain all the Current entries
Entry4_list = []
#list that contain all the On Time duration entries
Entry5_list = []
def dynamic_entry(index):
    #display the number as read only
    a_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=6, state='readonly',justify='center'))
    #add to grid
    a_list[index].grid(row=index + 1, column=0,)
    #display the x coordinates
    Entry1_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=6))
    #add to grid
    Entry1_list[index].grid(row=index + 1, column=1)
    #display the y coordinates
    Entry2_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=6))
    #add to grid
    Entry2_list[index].grid(row=index + 1, column=2)
    #display the capture selection drop down menu
    combobox_list.append(ttk.Combobox(frame2, width=15, values=(
        'CAPTURE', 'CAPTURE1', 'CAPTURE2', 'CAPTURE3', 'CAPTURE4', 'CAPTURE5'), state='readonly'))
    #add to grid
    combobox_list[index].grid(row=index + 1, column=3)
    #sets the drop box to the current capture selection value value
    combobox_list[index].current()
    #display the current(a) value
    Entry3_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=10))
    #add to grid
    Entry3_list[index].grid(row=index + 1, column=4)
    #display the voltage value
    Entry4_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=10))
    #add to grid
    Entry4_list[index].grid(row=index + 1, column=5)
    #display the warm up time value
    Entry5_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1, width=10))
    #add to grid
    Entry5_list[index].grid(row=index + 1, column=6)
# creating new frame for canvas
Main_Scrollbar_frame = LabelFrame(mainWindow, text="Input", width=400, height=200, pady=5, padx=5,
                                  font=('Arial', 16, "bold"), fg="#00adb5",background="#393e46")
# creating canvas and scrollbar to show multiple row and column Entries
canvas = Canvas(Main_Scrollbar_frame, bg='#eeeeee', width=1300, height=100)
scrollbar = ttk.Scrollbar(Main_Scrollbar_frame, orient=VERTICAL
                          , command=canvas.xview)
# configure the scrollbar at canvas
canvas.configure(yscrollcommand=scrollbar.set)
# binding the scrollbar at canvas
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# creating a new frame on canvas to display row and column Entries
frame2 = Frame(canvas, padx=2, pady=2)
frame2.config(bg="#eeeeee")
frame2.pack(side=TOP, pady=10, padx=5)
# creating a canvas window on frame2
canvas.create_window((0, 0), window=frame2, anchor='sw')
# configure scrollbar to show at the right side
scrollbar.config(command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="top", fill="x")
# Closing frame
Main_Scrollbar_frame.pack(side=TOP, padx=10, pady=10)
Label(frame2, text="Num:",  bg='#eeeeee',fg="#393e46",font=('Arial', 7, 'bold')).grid(row=0, column=0)
a = Label(frame2, text="X", bg='#eeeeee',fg="#393e46", font=('Arial', 7, 'bold')).grid(row=0, column=1)
b = Label(frame2, text="Y", bg='#eeeeee',fg="#393e46", font=('Arial', 7, 'bold')).grid(row=0, column=2)
c = Label(frame2, text="CAPTURE RANGE",  bg='#eeeeee',fg="#393e46",font=('Arial', 7, 'bold')).grid(row=0, column=3)
Label(frame2, text="VOLTAGE",  bg='#eeeeee',fg="#393e46",font=('Arial', 7, 'bold')).grid(row=0, column=4)
Label(frame2, text="CURRENT",  bg='#eeeeee',fg="#393e46",font=('Arial', 7, 'bold')).grid(row=0, column=5)
Label(frame2, text="WARM-UP TIME",  bg='#eeeeee',fg="#393e46",font=('Arial', 7, 'bold')).grid(row=0, column=6)
# function calling to insert first row and column entries
dynamic_entry(index) 
# function for update the scrollbar
def reset_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
#####-------/INPUT FRAME-------#####

#####-------OUTPUT FRAME-------#####
frame3 = tk.Frame(mainFrame, width=750, height=400)
frame3.pack(side=RIGHT, anchor=NE, padx=15, pady=5)
frame3_1=tk.Frame(frame3)
frame3_1.pack(fill='x')
frame3_2=tk.Frame(frame3)
frame3_2.pack(fill='x')
scrollbar = Scrollbar(frame3_1, orient=VERTICAL)
list_box = Listbox(frame3_1, selectmode="multiple", height=6, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
list_box.pack(fill='x', expand=1)
global canvas_xy
def polt_canvas():
    global canvas_xy
    canvas_xy = Canvas(frame3_2, bg='grey', width=700, height=300)
    canvas_xy.pack(side=TOP, fill="x")  # placing it on window
polt_canvas()
#####-------/OUTPUT FRAME-------#####

#####-------STATUS BAR-------#####
status = Label(mainWindow, text="status..",bd=1,relief=SUNKEN, anchor=W, background='#aad8d3')
status.pack(side=BOTTOM, fill=X)
#####-------/STATUS BAR-------#####

#home button
home_btn = PhotoImage(file=Path(__file__).parent / "images/home.png")
small2 = home_btn.subsample(30,30)
homeButt = Button(toolbar, command=lambda:[robotSer.write(b'G28 X Y\n'),status.config(text = "G28 Axis Homing...")], image=small2, highlightthickness = 0, bd = 0)
homeButt.pack(side=LEFT, padx=15, pady=10)
#----------- / WINDOW/FRAME SETUP-----------


#-----------FUNCTION SETUP-----------
#function to show video in frame
def show_frame():
    #reading cam
    ret, frame = cap.read()
    #converting color into cv2.COLOR_BGR2RGBA
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    rotated1 = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
    #giving size to the video/image screen
    img = Img.fromarray(rotated1).resize((400, 400))
    #add the image into tkinter
    imgtk = ImageTk.PhotoImage(image=img)
    #showing the image in tkinter window
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    #resetting the image after 10 ms
    lmain.after(10, show_frame)

#arrays for led analyser read data
xchromArray = []
ychromArray = []
intensityArray = []
csvArray = []

#plot for output intensity data
def plots():
    #Creating figure
    f = Figure(figsize=(7, 3.5), dpi=80) 
    #assigning a the add plot
    a = f.add_subplot(111)
    canvas_xy.destroy()
    polt_canvas()
    if len(intensityArray) != 0:
        index_list=[]
        for i in range(len(intensityArray)):
            index_list.append(i)
        print(index_list, c)
        a.xaxis.set_major_locator(MaxNLocator(integer=True))
        for i, txt in enumerate(intensityArray):
            a.annotate(txt, (index_list[i], intensityArray[i]))
        a.bar(index_list, intensityArray, color ='#00adb5')     
        a.set_ylabel("Intensity")
        a.set_xlabel("Measurement Number")
        #Creating canvas for plot
        canvas_1 = FigureCanvasTkAgg(f, master=canvas_xy)
        #showing plot
        canvas_1.draw()
        #placing canvas on window
        canvas_1.get_tk_widget().pack(pady=5, padx=5)
        status.config(text = "plotting...")
        mainWindow.update()

#read back from led analyser
def la_buffer_read():
    status.config(text = "reading LA buffer...")
    mainWindow.config(cursor="wait")
    num = laSer.inWaiting()
    #print('num bytes:',num)
    #list_box.insert(0,num)
    while laSer.inWaiting()>1:
        response2=laSer.readline()
        response3=response2.decode("utf-8")
        print(response3)
        n = 7
        split_strings = [response3[index : index + n] for index in range(0, len(response3), n)]
        print(split_strings)
        xchrom = split_strings[0]
        ychrom = split_strings[1]
        intensity = split_strings[2]
        xchromf = float(xchrom)
        xchromArray.append((xchromf))
        ychromf = float(ychrom)
        ychromArray.append((ychromf))
        intensityint = int(intensity)
        intensityArray.append((intensityint))
        print(xchromArray)
        print(ychromArray)
        print(intensityArray)
        response5 = len(intensityArray)-1,":", "X Chromaticity: ",xchromf,' | ',' Y Chromaticity: ',ychromf,' | ',' Intensity: ',intensityint
        response6 = str(response5)
        response7 = response6.replace('{','').replace('}','').replace('\'','').replace(',','').replace('(','').replace(')','')
        response4 = response7
        response8 = str(response4)
        csvArray.append((response8))
        status.config(text = response4)
        mainWindow.update()
        list_box.insert(len(intensityArray), response4 )
        laSer.flushInput()
    print('+++++++++++++++++++++++++++')
    time.sleep(1)

def saveButton():
    filename = filedialog.asksaveasfilename(initialdir='/', title='Save File', filetypes=[("CSV files", "*.csv")])
    textContent = "I'm the text in the file"
    name2 = filename + ".csv"
    myfile = open(name2, "w+")
    toWrite = ', '.join(csvArray)
    myfile.write(toWrite)
    print("File saved as ", filename)
#----------- / FUNCTION SETUP -----------


#----------- MAIN-----------
pos_listX = []  # creating list or array to store x and y axis
pos_listY = []  # creating list or array to store x and y axis
Capture_Selection=[]
Voltage_list = []
Current_list = []
On_time_duration_list = []
index = len(pos_listX)

# function to get the x and y axis of image
def getorigin(eventorigin):
    x0 = eventorigin.x  # storing x position in x0
    y0 = eventorigin.y  # storing y position in xy
    # storing x and y position in pos
    pos = 'X axis = ' + f'{x0}' + '   ' + 'Y axis = ' + f'{y0}'
    # combining x and y position for storing in array or list
    list_valueX = (x0)
    list_valueY = (y0)
    # inserting x and y position in list or array
    index = len(pos_listY)
    pos_listX.append((list_valueX))
    pos_listY.append((list_valueY))
    Entry1_list[index].insert(0, pos_listX[index])
    Entry2_list[index].insert(0, pos_listY[index])
    a_list[index].configure(state='normal')
    a_list[index].insert(0, index)
    a_list[index].configure(state='readonly')
    # inserting new row and col in frame2
    dynamic_entry(index + 1)
    # bind reset scrollbar function
    frame2.bind("<Configure>", reset_scrollregion) 
    l1 = Label(mainWindow, text='(' + f'{x0}' + ',' + f'{y0}' + ')', font=('Times New Roman', 7), bg='lightgray')
    l1.place(x=x0, y=y0)
    runButt.config(state="active")
# binding mouseclick event image
b = lmain.bind("<Button 1>", getorigin)
def bind():
    b
bind()
#https://stackoverflow.com/questions/37902503/unable-to-unbind-a-function-using-tkinter
def unbind():
    lmain.unbind("<Button 1>", b)
    
#checking datatype
def check(typee,data):
    checking = []
    for i in data:
        try:
            typee(i)
            checking.append(True)
        except:
            checking.append(False)
    if False in checking:
        return False
    else:
        return True

#####-------MAIN RUN BUTTON-------#####
def itterateCallBack():
    checks = []
    global index
    #mainWindow.config(cursor="wait")
    mainWindow.update()
    #send data ti the checks array
    for i in range(len(Entry1_list)-1):
        checks.append(Entry1_list[i].get())
        checks.append(Entry2_list[i].get())
        checks.append(Entry3_list[i].get())
        checks.append(Entry4_list[i].get())
        checks.append(Entry5_list[i].get())
        checks.append(combobox_list[i].get())
    #look for empty fields
    if '' in checks:
        messagebox.showwarning('Empty Fields', 'Please fill all input fields.')
    else:
        if check(int,checks[0::6])==True and check(int,checks[1::6])==True and check(float,checks[2::6])==True and check(float,checks[3::6])==True and check(float,checks[4::6])==True:
            new = Toplevel()
            x = mainWindow.winfo_x()
            y = mainWindow.winfo_y()
            new.geometry("+%d+%d" % (x + 300, y + 300))
            new.resizable(0,0)
            new.iconbitmap(Path(__file__).parent / "images/running.ico")
            title = i
            title2 = len(Entry1_list)-2
            title3 = title,"of",title2
            new.title(title3)
            def progresstitle():
                new.iconbitmap(Path(__file__).parent / "images/running.ico")
                title = i
                title2 = len(Entry1_list)-2
                title3 = title,"of",title2
                new.title(title3)
            s = ttk.Style()
            s.theme_use('clam')
            s.configure("red.Horizontal.TProgressbar", troughcolor ='#393e46', background="#00adb5", thickness=500)
            progress=Progressbar(new,style="red.Horizontal.TProgressbar",orient=HORIZONTAL,length=500,mode='determinate',)
            progress.grid(row=0,column=0,padx=30,pady=20)
            progresstitle()
            import time
            
            progress['value']=0
            new.update_idletasks()
            time.sleep(1)                       
            
            for i in range(len(pos_listY)):
                Capture_Selection.append(combobox_list[i].get())
                Voltage_list.append(Entry3_list[i].get())
                Current_list.append(Entry4_list[i].get())
                On_time_duration_list.append(Entry5_list[i].get())
            print(Capture_Selection)

            xprint1 = 0.5 * np.array(pos_listX)
            print("xprint1",xprint1)
            xprint2 = np.round(xprint1)
            print("xprint2",xprint2)
            xprint3 = [round(x) for x in xprint2]
            print(xprint3)
            yprint1 = -1 * np.array(pos_listY)
            yprint1half = yprint1 + 500
            yprintdivide = 0.5 * yprint1half 
            yprint2 = np.round(yprintdivide)
            yprint3 = [round(y) for y in yprint2]
            print(yprint3)
            #look up table
            for i, val in enumerate(yprint3):
                #x axis
                if xprint3[i] <=49:
                    xprint3[i] = xprint3[i]*1.10
                elif 50 < xprint3[i] < 56:
                    xprint3[i] = xprint3[i]*1.06
                elif 57 < xprint3[i] < 62:
                    xprint3[i] = xprint3[i]*1.035                   
                elif 63 < xprint3[i] < 68:
                    xprint3[i] = xprint3[i]*1.0106 
                elif 69 < xprint3[i] < 75:
                    xprint3[i] = xprint3[i]*1
                elif 76 < xprint3[i] < 81:
                    xprint3[i] = xprint3[i]*0.9867                    
                elif 82 < xprint3[i] < 88:
                    xprint3[i] = xprint3[i]*0.9815
                elif 89 < xprint3[i] < 94:
                    xprint3[i] = xprint3[i]*0.9771 
                elif 95 < xprint3[i] < 100:
                    xprint3[i] = xprint3[i]*0.9733
                elif 101 < xprint3[i] < 106:
                    xprint3[i] = xprint3[i]*0.97
                elif 107 < xprint3[i] < 113:
                    xprint3[i] = xprint3[i]*0.9624
                elif 114 < xprint3[i] < 119:
                    xprint3[i] = xprint3[i]*0.9556
                elif 120 < xprint3[i] < 125:
                    xprint3[i] = xprint3[i]*0.9495                  
                elif 125 < xprint3[i] < 131:
                    xprint3[i] = xprint3[i]*0.9440 
                elif 132 < xprint3[i] < 138:
                    xprint3[i] = xprint3[i]*0.9371 
                elif 139 < xprint3[i] < 144:
                    xprint3[i] = xprint3[i]*0.9309
                elif 145 < xprint3[i] < 150:
                    xprint3[i] = xprint3[i]*0.9252
                elif 150 < xprint3[i] < 160:
                    xprint3[i] = xprint3[i]*0.9200
                elif 160 < xprint3[i] < 200:
                    xprint3[i] = xprint3[i]*0.9000
                else:
                    xprint3[i] = xprint3[i]

                #y axis
                if yprint3[i] <=49:
                    yprint3[i] = yprint3[i]*1.2
                elif 50 < yprint3[i] < 75:
                    yprint3[i] = yprint3[i]*1.1
                elif 76 < yprint3[i] < 90:
                    yprint3[i] = yprint3[i]*1.05
                elif 91 < yprint3[i] < 100:
                    yprint3[i] = yprint3[i]*1.045
                elif 101 < yprint3[i] < 125:
                    yprint3[i] = yprint3[i]*1.05
                elif 126 < yprint3[i] < 131:
                    yprint3[i] = yprint3[i]*1.055
                elif 132 < yprint3[i] < 138:
                    yprint3[i] = yprint3[i]*1.0576
                elif 139 < yprint3[i] < 144:
                    yprint3[i] = yprint3[i]*1.0645
                elif 145 < yprint3[i] < 150:
                    yprint3[i] = yprint3[i]*1.0709
                elif 151 < yprint3[i] < 160:
                    yprint3[i] = yprint3[i]*1.0768
                elif 161 < yprint3[i] < 200:
                    yprint3[i] = yprint3[i]*1.085
                else:
                    yprint3[i] = yprint3[i]


                yprint3 = [round(y) for y in yprint3]
                xprint3 = [round(y) for y in xprint3]

                print(i, ",", xprint3[i], yprint3[i])
                #format x and y input to gcode
                xval = 'G0 X' + str(xprint3[i]) + ' Y' + str(yprint3[i])
                print(i)
                #format g-code to bytes for transmission to robot
                val = f'{xval}\n'
                import struct
                print(val)
                #update status bar
                status.config(text = xval)
                #update for progress bar
                mainWindow.update()
                #tell robot 'wait until move is finished before continuing'
                robotSer.write(b'M400\n')
                #transmit g-code to robot
                robotSer.write(bytes(val, 'UTF-8'))


                progress['value']=25
                progresstitle()
                new.update_idletasks()
                time.sleep(0.5)
                
                #POWER
                #format voltage to 2 decimal place
                vset1 = "{:.2F}".format(float(Voltage_list[i]))
                #format voltage for PS structure
                vset2 = "VSET1:"+str(vset1)
                #encode voltage for transmission
                bvsend= str.encode(vset2)
                print(bvsend)
                #transmit voltage to PS
                ser2.write(bvsend)
                #delay to ensure transmission
                time.sleep(0.25)
                #format current to 3 decimal place
                iset1 = "{:.3F}".format(float(Current_list[i]))
                #format current for PS structure
                iset2 = "ISET1:"+str(iset1)
                #encode current for transmission
                bisend= str.encode(iset2)
                print(bisend)
                #transmit current to PS
                ser2.write(bisend)
                #delay to ensure transmission
                time.sleep(0.25)
                #delay to ensure head has reached destination
                time.sleep(5)
                #turn ON powersupply
                ser2.write(b'OUT1')
                #take in warm up time from list
                onTime = On_time_duration_list[i]
                #convert to float
                onTimeInt = float(onTime)
                #delay the program from the required time
                time.sleep(onTimeInt)
                print("ON-TIME",i,onTimeInt)

                progress['value']=50
                progresstitle()
                new.update_idletasks()
                time.sleep(0.5)
                
                #CAPTURE
                #take in capture selection from input list
                Capture = f'{Capture_Selection[i]}\n'
                print(Capture)
                #update the status bar
                status.config(text = "capturing...")
                #update the window for progress bad
                mainWindow.update()
                #transmit the user defined capture value to the Feasa LED Analyser
                laSer.write(bytes(Capture, 'UTF-8'))
                time.sleep(5)
                laSer.flushInput()
                laSer.write(b'getxyi01\n')
                time.sleep(1)
                la_buffer_read()
                time.sleep(2)
                #turn off power supply
                ser2.write(b'OUT0')
                time.sleep(2)
                progress['value']=75
                new.update_idletasks()
                time.sleep(0.5)

                #-----------MEASUREMENT DB TABLE-----------
                xcoordinate = int(xprint3[i])
                ycoordinate = int(yprint3[i])
                current = Current_list[i]
                voltage = Voltage_list[i]
                warmUpTime = onTimeInt
                capture = Capture_Selection[i]
                outputIntensity = intensityArray[i]

                #connect to database
                conn = sqlite3.connect('FYP.db')
                #creat cursor abstraction
                c = conn.cursor()
                #turn on foreign key constraint
                c.execute("PRAGMA foreign_keys = ON")
                #create the table
                c.execute("CREATE TABLE IF NOT EXISTS measurements(measurement_id INTEGER PRIMARY KEY AUTOINCREMENT, datestamp1 TEXT, xcoordinate INTEGER, ycoordinate INTEGER, voltage TEXT, current TEXT, warmUpTime REAL, capture TEXT, outputIntensity INTEGER, foreign_key INTEGER, FOREIGN KEY(foreign_key) REFERENCES project(project_id))")
                #timestamp time
                unix1 = int(time.time())
                #add date
                datestamp1 = str(datetime.datetime.fromtimestamp(unix1).strftime('%Y-%m-%d %H:%M:%S'))
                #insert values
                c.execute("INSERT INTO measurements(datestamp1,xcoordinate, ycoordinate, voltage, current, warmUpTime, capture, outputIntensity, foreign_key) VALUES (?,?,?,?,?,?,?,?,?)",(datestamp1,xcoordinate, ycoordinate, voltage, current, warmUpTime, capture, outputIntensity, projectId))
                #commit to confirm insert
                conn.commit()

                progress['value']=100
                progresstitle()
                new.update_idletasks()
                time.sleep(0.5)

                if i == len(pos_listX)-1:
                    new.destroy()
                    runButt.config(state="disabled")
                    saveButt.config(state="normal")
                    unbind()
        
        
        else:
            messagebox.showwarning('Wrong Datatype', 'Please use the correct input datatype')
#####-------/ MAIN RUN BUTTON-------#####

    plots()
    mainWindow.config(cursor="")
    status.config(text = "DONE!")
    #home x and y axis
    robotSer.write(b'G28 X Y\n')

    #connect to db
    conn = sqlite3.connect('FYP.db')
    #creat cursor abstraction
    c = conn.cursor()
    #get number of measurements
    index = int(len(pos_listX))
    #insert the number of measurements into the database
    c.execute('''UPDATE project SET numMeasurements = ? WHERE datestamp = ?''',(index,datestamp))
    #commit the changes
    conn.commit()

show_frame()  # Display
mainWindow.mainloop()  # Starts GUI
