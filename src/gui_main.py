import tkinter as tk
from tkinter import tix
from tkinter.constants import *
from tkinter import filedialog
from tkinter.constants import W
import os
from functools import partial
from PIL import ImageTk, Image
import webbrowser
import time

# Grid settings
GRID_COL_NUM = 5
GRID_ROW_NUM = 10
PADDING = 5
# Widgets settings
E_WIDTH = 140
E_HEIGHT = 40
# Main windows settings
ZOOM_FACTOR = 1.4
WIN_WIDTH = int((E_WIDTH + PADDING) * GRID_COL_NUM + PADDING)
WIN_HEIGHT = int((E_HEIGHT + PADDING) * GRID_ROW_NUM + PADDING)
WIN_TITLE = 'Rice Disease Classifier'

# Root Settings

root = tix.Tk()
tip = tix.Balloon(root)
root.iconbitmap("src\icon.ico")
root.geometry(f"{int(WIN_WIDTH*ZOOM_FACTOR)}x{int(WIN_HEIGHT*ZOOM_FACTOR)}")
root.title(WIN_TITLE)
root.minsize(WIN_WIDTH, WIN_HEIGHT)
for x in range(GRID_COL_NUM):
    if x != GRID_COL_NUM - 1:
        root.grid_columnconfigure(x, weight=1, minsize=E_WIDTH)
    else:
        root.grid_columnconfigure(x, weight=0, minsize=E_WIDTH)

for y in range(GRID_ROW_NUM):
    root.grid_rowconfigure(y, weight=1, minsize=E_HEIGHT)

color_chart_win = None

# Functions

def open_select_source_image(canvas: tk.Canvas):
    filetypes = (
        ('Image file', '*.jpg;*.png'),
    )

    global filename
    filename = filedialog.askopenfilename(
        title='Import source image',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if len(filename)>0:
        clear()
        preview()

def openweb():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(url,new=1)


def clear():
    for widgets in root.winfo_children():
        widgets.grid_remove()

def welcome():
    titlelabel1.grid(row=2,columnspan=3,column=2)
    titlelabel2.grid(row=3,columnspan=3,column=2)
    helpbutton.grid(row=1,column=4)
    splash.grid(row=1,column=0,rowspan=7,columnspan=2)
    startbutton.grid(row=5,columnspan=3,column=2)

def help():
    splash.grid(row=1,column=0,rowspan=7,columnspan=2)
    helplabel1.grid(row=2,columnspan=3,column=2)
    helplabel2.grid(row=4,columnspan=3,column=2)
    helpbackButton.grid(row=1,column=4)

def preview():
    steplabel1.grid(row=2,column=0,columnspan=5)
    global img
    img = ImageTk.PhotoImage(Image.open(filename))
    importcanvas.create_image(0,0,anchor=W, image=img)
    importcanvas.grid(column=0, row=3,columnspan=5, padx=PADDING, pady=PADDING, sticky="nsew")
    analysebutton.grid(row=4,column=1,columnspan=5)
    changebutton.grid(row=4,column=1,columnspan=2)

def analyse():
    # ZS, the stepLabel2 doesnt show u p, idk why it cut straight to the result page llol
    steplabel1.grid_remove
    steplabel2.grid(row=2,column=0,columnspan=5)
    analysebutton.grid_remove
    changebutton.grid_remove
    time.sleep(3)
    results()

def results():
    clear()
    importcanvas.create_image(0,0,anchor=W, image=img)
    importcanvas.grid(column=0, row=3,columnspan=5, padx=PADDING, pady=PADDING, sticky="nsew")
    steplabel3.grid(row=2,column=0,columnspan=5)
    resultlabel.grid(row=4,column=0,columnspan=5)
    treatmentbutton.grid(row=5,column=1,columnspan=5)
    retrybutton.grid(row=5,column=1,columnspan=2)

# Widgets and shits

# Welcome page
splash = tk.Canvas(root, width=400, height=800)
splashimage = ImageTk.PhotoImage(Image.open("src\splash.jpg"))
splash.create_image(20,20, anchor=NW, image=splashimage)
importcanvas = tk.Canvas(root, width=400, height=400)
titlelabel1 = tk.Label(root, text="Rice Disease \nClassifer", font=("Arial Bold",32))
titlelabel2 = tk.Label(root, text='"Classifying Rice Diseases with Deep Learning"', font=("Arial",15),bg="black",fg="white")
helpbutton = tk.Button(root, text="?",font=("Arial Bold",24),padx=5,pady=5,command=lambda:[clear(),help()])
tip.bind_widget(helpbutton, balloonmsg="The program takes in your images and make predictions by passing it through the Machine Learning model we have trained.")
startbutton = tk.Button(root, text="Get Started",font=(9), padx=5,pady=5, command=partial(open_select_source_image, importcanvas))

# Help page
helplabel1 = tk.Label(root, text="What exactly is \nRice Disease \nClassifier? ", font=("Arial Bold",32))
helplabel2 = tk.Label(root, text='The program takes in your images and make predictions \nby passing it through the Machine Learning model \nwe have trained.', font=("Arial",12))
helpbackButton = tk.Button(root, text="<",font=("Arial Bold",24),padx=5,pady=5,command=lambda:[clear(),welcome()])

# Import page
steplabel1 = tk.Label(root, text="Image Preview", font=("Arial",24))
importbutton = tk.Button(root, text="Import Image",font=(9), command=partial(open_select_source_image, importcanvas))
tip.bind_widget(importbutton, balloonmsg="The program only accepts JPED and PNG imports. Sorry!")
changebutton = tk.Button(root, text="Change Image", font=(9), padx=5, command=partial(open_select_source_image, importcanvas))
analysebutton = tk.Button(root,text="Analyze", font = (9), padx=10, command=analyse)

# Analyse Page
steplabel2 = tk.Label(root, text="Processing the image. Please wait...", font=("Arial",24))

# Results Page
steplabel3 = tk.Label(root, text="Results", font=("Arial",24))
resultlabel = tk.Label(root, text="Detected: Healthy", font=("Green",15))
treatmentbutton = tk.Button(root, text="Suggested Treatments",font = (9), command=openweb)
tip.bind_widget(treatmentbutton, balloonmsg="Redirects you to a website on treatment information.")
retrybutton = tk.Button(root, text="Retry",font = (9), command=lambda:[clear(),welcome()])


welcome()
root.mainloop()