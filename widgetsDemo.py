from tkinter import *
import os
from PIL import ImageTk,Image


file2 = os.path.abspath('navi-2.png')
class WidgetsDemo():
    def __init__(self):
        window = Tk()
        window.title("Widgets Demo")

        file1 = ImageTk.PhotoImage(Image.open("navi-1.png"))  


        # Add check and radio button
        frame1 = Frame(window)
        frame1.pack(side = LEFT)
        self.name = "Richard Ticklin"
        self.v1 = IntVar()
        cbtBold = Checkbutton(frame1, text = "Bold",
                              variable = self.v1, command = self.processCheckButton)
        self.v2 = IntVar()
        rbRed = Radiobutton(frame1, text = "Red", bg = "red",
                            variable = self.v2, value = 1,
                            command = self.processRadioButton)
        
        rbYellow = Radiobutton(frame1, text =  "Yellow", bg = "yellow",
                               variable = self.v2, value = 2,
                               command = self.processRadioButton)
        cbtBold.grid(row = 1, column = 1)
        rbRed.grid(row = 1, column =2)
        rbYellow.grid(row = 1, column = 3)

        # Images
        frame2 = Frame(window)
        frame2.pack(side = RIGHT)
        # Image 1
        canvas1 = Canvas(frame2, width = 600, height = 400)  
        canvas1.pack(side = TOP)  
        img1 = ImageTk.PhotoImage(Image.open("navi-1.png"))  
        canvas1.create_image(20, 20, anchor=N, image=img1)
        # Image 2
        canvas2 = Canvas(frame2, width = 600, height = 400)  
        canvas2.pack(side = BOTTOM)  
        img2 = ImageTk.PhotoImage(Image.open("navi-1.png"))  
        canvas2.create_image(20, 20, anchor=N, image=img2) 

    def processCheckButton(self):
        print("check button is " +
              ("checked " if self.v1.get() == 1 else "unchecked"))

    def processRadioButton(self):
        print(("Red" if self.v2.get() == 1 else "Yellow") +
              " is selected ")

    def processButton(self):
        print("Your name is " + self.name.get())

WidgetsDemo()
