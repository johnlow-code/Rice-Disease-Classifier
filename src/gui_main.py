import tkinter as tk
from tkinter import tix
from tkinter.constants import *
from tkinter import filedialog
from tkinter.constants import W
import os
from functools import partial
from PIL import ImageTk, Image
import webbrowser

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

    filename = filedialog.askopenfilename(
        title='Import source image',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    global img
    img = ImageTk.PhotoImage(Image.open(filename))
    canvas.create_image(20,20, anchor=NW, image=img)
    canvas.grid(column=0, row=3, columnspan=5, rowspan=3, padx=PADDING, pady=PADDING, sticky="nsew")
    analyzeButton.grid(row=4,column=0)
    clearButton.grid(row=4,column=1)

def clearimport():
    analyzeButton.grid_remove()
    canvas.grid_remove()
    clearButton.grid_remove()
    
def fakeanalyse():
    stepLabel2.grid(row=5,column=0)
    stepLabel3.grid(row=6,column=0)
    resultLabel.grid(row=7,column=0)
    treatmentButton.grid(row=8,column=0)
    clearAllButton.grid(row=8,column=1)

def openweb():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(url,new=1)


    # if len(filename) > 0 and can_image:
    #     CLOTH_MATCHING.set_source_image(filename=filename, can_image=can_image, scroll_frame=scroll_frame)


def analyse():
    "ML Prediction Function here and get the answer as text string"
    ansLabel = Label(root, text="HISPA")
    ansLabel.pack()

def clearall():
    analyzeButton.grid_remove()
    canvas.grid_remove()
    clearButton.grid_remove()
    stepLabel2.grid_remove()
    stepLabel3.grid_remove()
    resultLabel.grid_remove()
    treatmentButton.grid_remove()
    clearAllButton.grid_remove()

# Widgets and shits
canvas = tk.Canvas(root, width=300, height=300)
titleLabel1 = tk.Label(root, text="Rice Disease Classifer", font=("Arial Bold",32),bg="black",fg="white")
titleLabel2 = tk.Label(root, text='"Classifying Rice Diseases with Deep Learning"', font=("Arial",15))
infoButton = tk.Button(root, text="?",font=("Arial Bold",24),padx=5,pady=5)
tip.bind_widget(infoButton, balloonmsg="The program takes in your images and make predictions by passing it through the Machine Learning model we have trained.")
stepLabel1 = tk.Label(root, text="1. Import the image", font=("Arial",24))
importButton = tk.Button(root, text="Import Image(s)",font=(9), command=partial(open_select_source_image, canvas))
tip.bind_widget(importButton, balloonmsg="The program only accepts JPED and PNG imports. Sorry!")
clearButton = tk.Button(root, text="Clear Import", font=(9), command=clearimport)
analyzeButton = tk.Button(root,text="Analyze", font = (9), command=fakeanalyse)
stepLabel2 = tk.Label(root, text="2. Processing the image...", font=("Arial",24))
stepLabel3 = tk.Label(root, text="3. Results", font=("Arial",24))
resultLabel = tk.Label(root, text="Detected: Healthy", font=("green",15))
treatmentButton = tk.Button(root, text="Suggested Treatments",font = (9), command=openweb)
tip.bind_widget(treatmentButton, balloonmsg="Redirects you to a website on treatment information.")
clearAllButton = tk.Button(root, text="Retry",font = (9), command=clearall)

titleLabel1.grid(row=0,columnspan=5,column=0)
titleLabel2.grid(row=1,columnspan=5,column=0)
infoButton.grid(row=0,column=5)
stepLabel1.grid(row=2,column=0)
importButton.grid()

root.mainloop()