import tkinter as tk
from tkinter import tix
from tkinter.constants import *
from tkinter import filedialog
import os
from functools import partial
from PIL import ImageTk, Image
import webbrowser
import random
from prediction import predict

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
icon = "src\icon.ico"
root = tix.Tk()
tip = tix.Balloon(root)
root.iconbitmap(icon)
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

def change_select_source_image(canvas: tk.Canvas):
    filetypes = (
        ('Image file', '*.jpg;*.png'),
    )
    global filename
    tempfilename = filename
    filename = filedialog.askopenfilename(
        title='Import source image',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    if len(filename) > 0:
        clear()
        preview()

    else:
        filename=tempfilename

def analyse():
    global probpercentage
    probpercentage = predict(filename)
    # probpercentage = [['Healthy',0.90],['LeafBlast',0.05],['BrownSpot',0.03],['Hispa',0.02]]
    print(probpercentage)
    stepLabel1.grid_remove
    stepLabel2.grid(row=2, column=0, columnspan=5)
    analyseButton.grid_remove
    changeButton.grid_remove
    results()


def results():
    clear()
    show_image(img)
    # importcanvas.create_image(0,0,anchor=W, image=img)
    # importcanvas.grid(column=0, row=3,columnspan=5, padx=PADDING, pady=PADDING, sticky="nsew")
    res = findMax(probpercentage)
    if disease == "Healthy":
        resultsLabel = tk.Label(root, text="The rice plant " + res + ".", bg="#ffd580", fg="green", font=(9))
    else:
        resultsLabel = tk.Label(root, text="The rice plant " + res + ".", bg="#ffd580", fg="#ff4500", font=(9))
    resultsLabel.grid(row=4, column=0, columnspan=5)
    stepLabel3.grid(row=2, column=0, columnspan=5)
    # resultLabel.grid(row=4,column=0,columnspan=5)
    showmoreButton = tk.Button(root, text="Show more", bg='#8d6713', fg='white', activebackground='white',
                               activeforeground='#8d6713', font=(9),
                               command=lambda: [showmore(), showmoreButton.grid_remove(), resultsLabel.grid_remove()])
    showmoreButton.grid(row=5, column=0, columnspan=5)
    if disease == "Healthy":
        pass
    else:
        treatmentButton.grid(row=10, column=0, columnspan=5)
    retryButton.grid(row=8, column=0, columnspan=4)
    menuButton.grid(row=8,column=1,columnspan=4)    
    
    emptyText.grid(row=12,column=0,columnspan=5)

    def showmore():
        summary = summariseProb(probpercentage)
        if disease == "Healthy":
            pLabel = tk.Label(root, text=summary,bg="#ffd580", fg="green", font=(9))
        else:
            pLabel = tk.Label(root, text=summary,bg="#ffd580", fg="#ff4500", font=(9))
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
        summary += p[0] + ": " + str(p[1]) + "\n"
    return summary


def findMax(prob):
    global disease
    disease = prob[0][0]
    if disease == "BrownSpot":
        return "most probably has Brown Spot"
    elif disease == "Healthy":
        return "is most probably Healthy"
    elif disease == "Hispa":
        return "most probably has Hispa"
    elif disease == "LeafBlast":
        return "most probably has Leaf Blast"


def openweb():
    # url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url = ""
    if disease == "BrownSpot":
        url = "http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/brown-spot"
    elif disease == "Healthy":
        pass
    elif disease == "Hispa":
        url = "http://www.agritech.tnau.ac.in/expert_system/paddy/cppests_ricehispa.html"
    elif disease == "LeafBlast":
        url = "https://www2.ipm.ucanr.edu/agriculture/rice/Rice-Blast/"
    webbrowser.open(url, new=1)


def treatment():
    if disease == "BrownSpot":
        disease1.grid(row=0, column=0, columnspan=5)
        treatmentTitle.grid(row=1, column=0, columnspan=5)
        trtDisease1.grid(row=2, column=0, columnspan=7)
        preventionTitle.grid(row=5, column=0, columnspan=5)
        pvtDisease1.grid(row=6, column=0, columnspan=7)
        linkButton = tk.Button(root, text="Click for more info", bg='#8d6713', fg='white', activebackground='white',
                               activeforeground='#8d6713', font=(9), command=openweb)
        tip.bind_widget(linkButton, balloonmsg="Redirects you to a website on treatment information.")
        linkButton.grid(row=8, column=2, columnspan=4)
        resultsButton.grid(row=8, column=1, columnspan=1)   
        menuButton.grid(row=10 ,column=0, columnspan=5) 
        emptyText.grid(row=12,column=0,columnspan=5)
        
    elif disease == "Healthy":
        pass
    elif disease == "Hispa":
        disease2.grid(row=0, column=0, columnspan=5)
        treatmentTitle.grid(row=1, column=0, columnspan=5)
        trtDisease2.grid(row=2, column=0, columnspan=7)
        preventionTitle.grid(row=5, column=0, columnspan=5)
        pvtDisease2.grid(row=6, column=0, columnspan=7)
        linkButton = tk.Button(root, text="Click for more info", bg='#8d6713', fg='white', activebackground='white',
                               activeforeground='#8d6713', font=(9), command=openweb)
        tip.bind_widget(linkButton, balloonmsg="Redirects you to a website on treatment information.")
        linkButton.grid(row=8, column=2, columnspan=4)
        resultsButton.grid(row=8, column=1, columnspan=1)   
        menuButton.grid(row=10 ,column=0, columnspan=5) 
        emptyText.grid(row=12,column=0,columnspan=5)
    elif disease == "LeafBlast":
        disease3.grid(row=0, column=0, columnspan=5)
        treatmentTitle.grid(row=1, column=0, columnspan=5)
        trtDisease3.grid(row=2, column=0, columnspan=7)
        preventionTitle.grid(row=5, column=0, columnspan=5)
        pvtDisease3.grid(row=6, column=0, columnspan=7)
        linkButton = tk.Button(root, text="Click for more info", bg='#8d6713', fg='white', activebackground='white',
                               activeforeground='#8d6713', font=(9), command=openweb)
        tip.bind_widget(linkButton, balloonmsg="Redirects you to a website on treatment information.")
        linkButton.grid(row=8, column=2, columnspan=4)
        resultsButton.grid(row=8, column=1, columnspan=1)   
        menuButton.grid(row=10 ,column=0, columnspan=5) 
        emptyText.grid(row=12,column=0,columnspan=5)


# Widgets and shits

# Welcome page
splash = tk.Canvas(root, width=400, height=800)
main_menu_img = 'src\splash.jpg'
splashimage = ImageTk.PhotoImage(Image.open(main_menu_img))
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
                         command=partial(change_select_source_image, importcanvas))
analyseButton = tk.Button(root, text="Analyze", font=(9), padx=10, bg='#8d6713', fg='white', activebackground='white',
                          activeforeground='#8d6713', command=analyse)

# Analyse Page
stepLabel2 = tk.Label(root, text="Processing the image. Please wait...", font=("Arial Bold", 24), bg="#fcf3cf",
                      fg="#8d6713")

# Results Page
stepLabel3 = tk.Label(root, text="Results", font=("Arial Bold", 24), bg="#fcf3cf", fg="#8d6713")
summary = ""
treatmentButton = tk.Button(root, text="Suggested Treatments", bg='#8d6713', fg='white', activebackground='white',
                            activeforeground='#8d6713', font=(9), command=lambda: [clear(), treatment()])
tip.bind_widget(treatmentButton, balloonmsg="Redirects you for more info.")
retryButton = tk.Button(root, text="Retry", font=(9), bg='#8d6713', fg='white', activebackground='white',
                        activeforeground='#8d6713', command=lambda: [open_select_source_image(importcanvas)])
menuButton = tk.Button(root, text="Main Menu", font=(9), bg='#8d6713', fg='white', activebackground='white',
                        activeforeground='#8d6713', command=lambda: [clear(),welcome()])

# Treatment Page
treatmentTitle = tk.Label(root, text="Treatment", font=("Arial Bold", 20), bg="#fcf3cf", fg="#8d6713")
preventionTitle = tk.Label(root, text="Prevention", font=("Arial Bold", 20), bg="#fcf3cf", fg="#8d6713")

disease1 = tk.Label(root, text="Brown Spot", font=("Arial Bold", 32), bg="#fcf3cf", fg="#8d6713")
trtDisease1 = tk.Label(root,
                       text='-Use resistant varieties.\n-Use fungicides (e.g., iprodione, propiconazole, azoxystrobin, trifloxystrobin, and carbendazim) as seed treatments.\n-Treat seeds with hot water (53−54°C) for 10−12 minutes before planting, to control primary infection at the seedling stage. \nTo increase effectiveness of treatment, pre-soak seeds in cold water for eight hours.\n',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")
pvtDisease1 = tk.Label(root,
                       text='-Use resistant varieties. \n-Apply required fertilizers\n-Apply calcium silicate slag before planting',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")

disease2 = tk.Label(root, text="Hispa", font=("Arial Bold", 32), bg="#fcf3cf", fg="#8d6713")
trtDisease2 = tk.Label(root,
                       text='-Spraying of methyl parathion 0.05percent or Quinalphos 0.05%\n-Spray neem based pesticide e.g. altineem @ 3ml per litre of water or crude neem seed oil.\n-Spray malathion 50percent EC @ 2ml per litre water when 1 adult or 1-2 damaged leaves per hill are seen',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")
pvtDisease2 = tk.Label(root,
                       text='-Avoid over fertilizing the field.\n-Leaf tip containing blotch mines should be destroyed.\n-Manual collection and killing of beetles\n-Clipping and burying shoots in the mud',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")

disease3 = tk.Label(root, text="Leaf Blast", font=("Arial Bold", 32), bg="#fcf3cf", fg="#8d6713")
trtDisease3 = tk.Label(root, text='-Applying fungicides at precise times of the plant’s development',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")
pvtDisease3 = tk.Label(root,
                       text='-Keep rice fields flooded deeply with a continual flow of water\n-Plant only certified disease-free seed of rice blast resistant rice plants\n-Incorporate or roll the rice stubble soon after harvest to promote early decomposition.\n-Avoid excessive nitrogen application rates and apply no more than 30 pounds per acre of nitrogen per application at midseason.',
                       font=("Arial", 12), bg="#fcf3cf", fg="#8d6713")
resultsButton = tk.Button(root, text="Back to results", font=(9), bg='#8d6713', fg='white', activebackground='white',
                        activeforeground='#8d6713', command=results)

emptyText = tk.Label(root, text="", font=("Arial Bold", 32), bg="#fcf3cf", fg="#fcf3cf")

welcome()
root.mainloop()
