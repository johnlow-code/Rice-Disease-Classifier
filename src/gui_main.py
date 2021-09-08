import tkinter as tk
from tkinter import *
from tkinter import tix
from tkinter.constants import *
from tkinter import filedialog
import os
from functools import partial
from PIL import ImageTk, Image
import webbrowser
import random
from prediction import predict
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

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
root.iconbitmap("C:\\Users\JxH\PycharmProjects\Rice-Disease-Classifier\src\icon.ico")
root.geometry(f"{int(WIN_WIDTH * ZOOM_FACTOR)}x{int(WIN_HEIGHT * ZOOM_FACTOR)}")
root.config(bg="#fcf3cf")
root.title(WIN_TITLE)
root.minsize(WIN_WIDTH, WIN_HEIGHT)
for x in range(GRID_COL_NUM):
    if x != GRID_COL_NUM - 1:
        root.grid_columnconfigure(x, weight=1, minsize=E_WIDTH)
    else:
        root.grid_columnconfigure(x, weight=0, minsize=E_WIDTH)

for y in range(GRID_ROW_NUM):
    root.grid_rowconfigure(y, weight=1, minsize=E_HEIGHT)

res = []
for i in range(4):
    res.append(random.random())

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

    if len(filename) > 0:
        clear()
        preview()


def openweb():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(url, new=1)


def clear():
    for widgets in root.winfo_children():
        widgets.grid_remove()


def welcome():
    titleLabel1.grid(row=2, columnspan=3, column=2)
    titleLabel2.grid(row=3, columnspan=3, column=2)
    helpButton.grid(row=1, column=4)
    howtoButton.grid(row=6, columnspan=3, column=2)
    splash.grid(row=1, column=0, rowspan=7, columnspan=2)
    startButton.grid(row=5, columnspan=3, column=2)


def help():
    splash.grid(row=1, column=0, rowspan=7, columnspan=2)
    helpLabel1.grid(row=2, columnspan=3, column=2)
    helpLabel2.grid(row=4, columnspan=3, column=2)
    helpBackButton.grid(row=1, column=4)


def howto():
    splash.grid(row=1, column=0, rowspan=7, columnspan=2)
    howtoLabel1.grid(row=2, columnspan=3, column=2)
    howtoLabel2.grid(row=4, columnspan=3, column=2)
    helpBackButton.grid(row=1, column=4)


def resize_image(image):
    resized_img = image.resize((500, 500))
    resized_img = ImageTk.PhotoImage(resized_img)
    return resized_img


def show_image(image):
    imgLabel = tk.Label(root, image=image)
    imgLabel.grid(row=3, column=2)


def preview():
    stepLabel1.grid(row=2, column=0, columnspan=5)
    global img
    img = Image.open(filename)
    img = resize_image(img)
    show_image(img)
    # importcanvas.create_image(0,0,anchor="center", image=img)
    # importcanvas.place(relx=0.5, rely=0.5, anchor="center")
    analyseButton.grid(row=6, column=1, columnspan=5)
    changeButton.grid(row=6, column=1, columnspan=2)


def analyse():
    global probpercentage
    probpercentage = predict(filename)
    print(probpercentage)
    stepLabel1.grid_remove
    stepLabel2.grid(row=2, column=0, columnspan=5)
    analyseButton.grid_remove
    changeButton.grid_remove
    # time.sleep(3)
    results()


def results():
    clear()
    show_image(img)
    # importcanvas.create_image(0,0,anchor=W, image=img)
    # importcanvas.grid(column=0, row=3,columnspan=5, padx=PADDING, pady=PADDING, sticky="nsew")
    resultsLabel = tk.Label(root, text="The rice plant " + findMax(probpercentage) + ".", font=(9))
    resultsLabel.grid(row=4, column=0, columnspan=5)
    stepLabel3.grid(row=2, column=0, columnspan=5)
    # resultLabel.grid(row=4,column=0,columnspan=5)
    showmoreButton = tk.Button(root, text="Show more", bg='#8d6713', fg='white', activebackground='white',
                               activeforeground='#8d6713', font=(9),
                               command=lambda: [showmore(), showmoreButton.grid_remove(), resultsLabel.grid_remove()])
    showmoreButton.grid(row=5, column=0, columnspan=5)
    treatmentButton.grid(row=8, column=2, columnspan=5)
    retryButton.grid(row=8, column=1, columnspan=2)

    def showmore():
        summary = summariseProb(probpercentage)
        pLabel = tk.Label(root, text=summary, font=(9))
        pLabel.grid(row=4, column=0, columnspan=5, rowspan=3)
        showlessButton = tk.Button(root, text="Show less", bg='#8d6713', fg='white', activebackground='white',
                                   activeforeground='#8d6713', font=(9), command=lambda: [pLabel.grid_remove(),
                                                                                          showlessButton.grid_remove(),
                                                                                          showmoreButton.grid(row=5,
                                                                                                              column=0,
                                                                                                              columnspan=5),
                                                                                          resultsLabel.grid(row=4,
                                                                                                            column=0,
                                                                                                            columnspan=5)])
        showlessButton.grid(row=7, column=0, columnspan=5)
    # def showless():
    #     pLabel.grid_remove()
    #     showlessButton.grid_remove()
    #     showmoreButton.grid(row=7,column=0,columnspan=5)


# def arrayPercentage(prob):
#     for i in range(len(prob[0])):
#         prob[0][i]=round((prob[0][i]*100),2)
#     return prob

def summariseProb(prob):
    summary = ""
    for p in prob:
        temptagname = p[0]
        if temptagname == 'BrownSpot':
            temptagname = 'Brown Spot'
        elif temptagname == 'LeafBlast':
            temptagname = 'Leaf Blast'
        summary += temptagname + ": " + str(p[1]) + "%\n"
    return summary


def findMax(prob):
    disease = prob[0][0]
    if disease == "BrownSpot":
        return "most probably has Brown Spot"
    elif disease == "Healthy":
        return "is most probably Healthy"
    elif disease == "Hispa":
        return "most probably has Hispa"
    elif disease == "LeafBlast":
        return "most probably has Leaf Blast"


def clear_result():
    res = []
    for i in range(4):
        res.append(random.random())


# Widgets and shits

# Welcome page
splash = tk.Canvas(root, width=400, height=800)
splashimage = ImageTk.PhotoImage(Image.open("C:\\Users\JxH\PycharmProjects\Rice-Disease-Classifier\src\splash.jpg"))
splash.create_image(20, 20, anchor=NW, image=splashimage)
importcanvas = tk.Canvas(root, width=400, height=400)
titleLabel1 = tk.Label(root, text="Rice Disease \nClassifer", font=("Arial Bold", 32), bg="#fcf3cf", fg="#8d6713")
titleLabel2 = tk.Label(root, text='"Classifying Rice Diseases with Deep Learning"', font=("Arial", 15), bg="#fcf3cf",
                       fg="#8d6713")
helpButton = tk.Button(root, text="i", font=("Arial Bold", 24), padx=5, pady=5, bg='#8d6713', fg='white',
                       activebackground='white', activeforeground='#8d6713', command=lambda: [clear(), help()])
tip.bind_widget(helpButton,
                balloonmsg="The program takes in your images and make predictions by passing it through the Machine Learning model we have trained.")
startButton = tk.Button(root, text="Get Started", font=("Arial Bold", 15), padx=5, pady=5, bg='#8d6713', fg='white',
                        activebackground='white', activeforeground='#8d6713',
                        command=partial(open_select_source_image, importcanvas))
howtoButton = tk.Button(root, text="How to use", font=("Arial", 15), padx=5, pady=5, bg='#8d6713', fg='white',
                        activebackground='white', activeforeground='#8d6713', command=lambda: [clear(), howto()])

# How to: page
howtoLabel1 = tk.Label(root, text="How to use \nRice Disease \nClassifier? ", font=("Arial Bold", 32), bg="#fcf3cf",
                       fg="#8d6713")
howtoLabel2 = tk.Label(root, text='1.Import the image \n2.Analyse \n3.View the result!', font=("Arial", 18),
                       bg="#fcf3cf", fg="#8d6713")

# Help page
helpLabel1 = tk.Label(root, text="What exactly is \nRice Disease \nClassifier? ", font=("Arial Bold", 32), bg="#fcf3cf",
                      fg="#8d6713")
helpLabel2 = tk.Label(root,
                      text='The program takes in your images and make predictions \nby passing it through the Machine Learning model \nwe have trained.',
                      font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")
helpBackButton = tk.Button(root, text="<", font=("Arial Bold", 24), padx=5, pady=5, bg='#8d6713', fg='white',
                           activebackground='white', activeforeground='#8d6713', command=lambda: [clear(), welcome()])

# Import page
stepLabel1 = tk.Label(root, text="Image Preview", font=("Arial Bold", 24), bg="#fcf3cf", fg="#8d6713")
importButton = tk.Button(root, text="Import Image", font=(9), bg='#8d6713', fg='white', activebackground='white',
                         activeforeground='#8d6713', command=partial(open_select_source_image, importcanvas))
tip.bind_widget(importButton, balloonmsg="The program only accepts JPED and PNG imports. Sorry!")
changeButton = tk.Button(root, text="Change Image", font=(9), padx=5, bg='#8d6713', fg='white',
                         activebackground='white', activeforeground='#8d6713',
                         command=partial(open_select_source_image, importcanvas))
analyseButton = tk.Button(root, text="Analyze", font=(9), padx=10, bg='#8d6713', fg='white', activebackground='white',
                          activeforeground='#8d6713', command=analyse)

# Analyse Page
stepLabel2 = tk.Label(root, text="Processing the image. Please wait...", font=("Arial Bold", 24), bg="#fcf3cf",
                      fg="#8d6713")

# Results Page
stepLabel3 = tk.Label(root, text="Results", font=("Arial Bold", 24), bg="#fcf3cf", fg="#8d6713")
summary = ""
# res_index = res.index(max(res))
# if (res_index == 0):
#     resultLabel = tk.Label(root, text="Detected: Brown Spot", font=("Brown",15), bg="#fcf3cf",fg="Brown")
# elif(res_index == 1):
#     resultLabel = tk.Label(root, text="Detected: Healthy", font=("Green",15), bg="#fcf3cf",fg="Green")
# elif(res_index == 2):
#     resultLabel = tk.Label(root, text="Detected: Hispa", font=("Red",15), bg="#fcf3cf",fg="Red")
# else:
#     resultLabel = tk.Label(root, text="Detected: Leaf Blast", font=("Yellow",15), bg="#fcf3cf",fg="Yellow")
treatmentButton = tk.Button(root, text="Suggested Treatments", bg='#8d6713', fg='white', activebackground='white',
                            activeforeground='#8d6713', font=(9), command=openweb)
tip.bind_widget(treatmentButton, balloonmsg="Redirects you to a website on treatment information.")
retryButton = tk.Button(root, text="Retry", font=(9), bg='#8d6713', fg='white', activebackground='white',
                        activeforeground='#8d6713', command=lambda: [clear(), welcome(), clear_result()])

# model = tf.keras.models.load_model('src\rice_disease_classifer_v1_test_7728.model')

welcome()
root.mainloop()
