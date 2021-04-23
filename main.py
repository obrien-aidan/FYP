"""
REFERENCE 1 = https://github.com/ajinkyapadwad/OpenCV-with-Tkinter/blob/master/video.py
"""
#-----------INPUT-----------
import cv2
from cv2 import cv2
import tkinter as tk
from tkinter import *
from PIL import Image as Img
from PIL import ImageTk
import serial
import time
#from serial import Serial
import serial
import time
import numpy as np
from tkinter import ttk
from matplotlib import pyplot as plt
#----------- / INPUT-----------

#-----------PORT SETUP-----------
ser = serial.Serial("COM7", 250000) #robto
ser1 = serial.Serial("COM5", 57600) #LA
# starting camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_EXPOSURE, -5.5)
#----------- / PORT SETUP-----------


#-----------WINDOW/FRAME SETUP-----------
# Window
white = "#ffffff"
lightBlue2 = "#305f72"
font = "Constantia"
fontButtons = (font, 12)
mainWindow = tk.Tk()
mainWindow.configure(bg=lightBlue2)
w = mainWindow.winfo_screenwidth()
h = mainWindow.winfo_screenheight() - 10
mainWindow.geometry("%dx%d+0+0" % (w, h))

# creating Frame for video
mainFrame = Frame(mainWindow, bg=lightBlue2)
mainFrame.pack(side=TOP, anchor=CENTER, fill='x')
lmain = tk.Label(mainFrame, cursor='crosshair')  # change the cursor into crosshair
lmain.pack(side=LEFT, anchor=NW, padx=5, pady=5)

# creating 2nd frame
global index
index = 0  # first index
Entry1_list = []  # list that contain all the X entries
Entry2_list = []  # list that contain all the Y entries
combobox_list = []  # list that contain all the combo-box

def dynamic_entry(index):
    Entry1_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1))
    Entry1_list[index].grid(row=index + 1, column=0)
    Entry2_list.append(Entry(frame2, font=("Arial", 10, 'bold'), bd=1))
    Entry2_list[index].grid(row=index + 1, column=1)
    combobox_list.append(ttk.Combobox(frame2, width=20, values=(
        'CAPTURE', 'CAPTURE1', 'CAPTURE2', 'CAPTURE3', 'CAPTURE4', 'CAPTURE5'), state='readonly'))
    combobox_list[index].grid(row=index + 1, column=2)
    combobox_list[index].current()

# creating new frame for canvas
Main_Scrollbar_frame = LabelFrame(mainWindow, text="Input", width=400, height=200, pady=5, padx=5,
                                  bg='White', font=('Arial', 16, "bold"))
# creating canvas and scrollbar to show multiple row and column Entries
canvas = Canvas(Main_Scrollbar_frame, bg='lightblue', width=430, height=100)
scrollbar = ttk.Scrollbar(Main_Scrollbar_frame, orient=VERTICAL
                          , command=canvas.xview)
# configure the scrollbar at canvas
canvas.configure(yscrollcommand=scrollbar.set)
# binding the scrollbar at canvas
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
# creating a new frame on canvas to display row and column Entries
frame2 = Frame(canvas, padx=2, pady=2)
frame2.config(bg="White")
frame2.pack(side=TOP, pady=10, padx=5)
# creating a canvas window on frame2
canvas.create_window((0, 0), window=frame2, anchor='sw')
# configure scrollbar to show at the right side
scrollbar.config(command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="top", fill="x")
# Closing frame
Main_Scrollbar_frame.pack(side=TOP, padx=10, pady=10)
a = Label(frame2, text="X", font=('Arial', 10, 'bold')).grid(row=0, column=0)
b = Label(frame2, text="Y", font=('Arial', 10, 'bold')).grid(row=0, column=1)
c = Label(frame2, text="CAPTURE RANGE", font=('Arial', 10, 'bold')).grid(row=0, column=2)
# function calling to insert first row and column entries
dynamic_entry(index) 
# function for update the scrollbar
def reset_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


#  creating Frame3 (right)
frame3 = tk.Frame(mainFrame, width=650, height=400)
frame3.pack(side=RIGHT, anchor=NE, padx=15, pady=5)
scrollbar = Scrollbar(frame3, orient=VERTICAL)
list_box = Listbox(frame3, selectmode="multiple", height=25, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
list_box.pack(fill='x', expand=1)
#----------- / WINDOW/FRAME SETUP-----------

#-----------FUNCTION SETUP-----------
# function to show image in frame
def show_frame():
    ret, frame = cap.read()  # reading cam
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # converting color into cv2.COLOR_BGR2RGBA
    rotated1 = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
    img = Img.fromarray(rotated1).resize((400, 400))  # giving size to the video/image screen
    imgtk = ImageTk.PhotoImage(image=img)  # add the image into tkinter
    # showing the image in tkinter window
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    # resetting the image after 10 ms
    lmain.after(10, show_frame)

# arrays for led analyser read data
xchromArray = []
ychromArray = []
intensityArray = []
def plots():
    if len(intensityArray) != 0:
        index_list=[]
        for i in range(len(intensityArray)):
            index_list.append(i)
        plt.close()
        plt.plot(index_list, intensityArray)
        plt.title("Plot Graph")
        plt.ylabel("Intensity")
        plt.xlabel("Index")
        plt.show()





# read back from led analyser
def la_buffer_read():
    time.sleep(1)
    num = ser1.inWaiting()
    #print('num bytes:',num)
    #list_box.insert(0,num)
    while ser1.inWaiting()>1:
        response2=ser1.readline()
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
        list_box.insert(0, response3)
        ser1.flushInput()
        plt.show()
    print('+++++++++++++++++++++++++++')
    time.sleep(1)

# start button
startButton = Button(mainWindow, text="START", font=fontButtons, bg=white, width=20, height=1, command=lambda :itterateCallBack())
startButton.pack(side=TOP)

#----------- / FUNCTION SETUP -----------

#----------- MAIN-----------
pos_listX = []  # creating list or array to store x and y axis
pos_listY = []  # creating list or array to store x and y axis
Capture_Selection=[]

# function to get the x and y axis of image
def getorigin(eventorigin):
    x0 = eventorigin.x  # storing x position in x0
    y0 = eventorigin.y  # storing y position in xy
    # storing x and y position in pos
    pos = 'X axis = ' + f'{x0}' + '   ' + 'Y axis = ' + f'{y0}'
    # entryTexta1.set( x0 )
    # entryTextb1.set( y0 )

    # combining x and y position for storing in array or list
    list_valueX = (x0)
    list_valueY = (y0)
    # inserting x and y position in list or array
    index = len(pos_listY)
    pos_listX.append((list_valueX))
    pos_listY.append((list_valueY))
    Entry1_list[index].insert(0, pos_listX[index])
    Entry2_list[index].insert(0, pos_listY[index])
    dynamic_entry(index + 1)  # inserting new row and col in frame2
    frame2.bind("<Configure>", reset_scrollregion)  # bind reset scrollbar function
    l1 = Label(mainWindow, text='(' + f'{x0}' + ',' + f'{y0}' + ')', font=('Times New Roman', 7), bg='lightgray')
    l1.place(x=x0, y=y0)



# binding mouseclick event image
lmain.bind("<Button 1>", getorigin)

# button itterate
def itterateCallBack():
    print('hello')
    for i in range(len(pos_listY)):
        Capture_Selection.append(combobox_list[i].get())
    print(Capture_Selection)
    xprint1 = 0.25 * np.array(pos_listX)
    xprint2 = np.round(xprint1)
    xprint3 = [round(x) for x in xprint2]
    yprint1 = 0.25 * np.array(pos_listY)
    yprint2 = np.round(yprint1)
    yprint3 = [round(y) for y in yprint2]
    for i, val in enumerate(yprint3):
        #G-CODE
        print(i, ",", xprint3[i], yprint3[i])
        xval = 'G1 X' + str(xprint3[i]) + ' Y' + str(yprint3[i])
        print(i)
        val = f'{xval}\n'
        import struct
        print(val)
        ser.write(b'm400\n')
        ser.write(bytes(val, 'UTF-8'))
        #CAPTURE
        Capture = f'{Capture_Selection[i]}\n'
        print(Capture)
        ser1.write(bytes(Capture, 'UTF-8'))
        time.sleep(5)
        ser1.flushInput()
        ser1.write(b'getxyi01\n')
        time.sleep(1)
        la_buffer_read()
    plots()


""" # start button
startButton = Button(mainWindow, text="START", font=fontButtons, bg=white, width=20, height=1, command=itterateCallBack)
startButton.pack(side=TOP) """


show_frame()  # Display
mainWindow.mainloop()  # Starts GUI
