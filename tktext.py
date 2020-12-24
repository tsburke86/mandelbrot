from tkinter import *
import os
from PIL import ImageTk,Image

class Mandelbrot():
    def __init__(self):
        window = Tk()
        window.title("Mandelbrot Navigator v4.20"
        # Left Side
        frame1 = Frame(window)
        frame1.pack(side = LEFT)
        Label(frame1, text = printDetails()).grid(row = 1, column = 1,  sticky = "W")
        Label(frame1, text = "Hey").grid(row = 2, column = 1)
        Label(frame1, text = "Hey").grid(row = 3, column = 1)



        # Right Side
        frame2 = Frame(window)
        frame2.pack(side = RIGHT)
        # Image 1
        canvas1 = Canvas(frame2, width = 600, height = 400)  
        canvas1.pack()  
        img1 = ImageTk.PhotoImage(Image.open("navi-1.png"))  
        canvas1.create_image(10, 10, anchor=NW, image=img1)
        # Image 2
        canvas2 = Canvas(frame2, width = 600, height = 400)  
        canvas2.pack(side = BOTTOM)  
        img2 = ImageTk.PhotoImage(Image.open("navi-2.png"))  
        canvas2.create_image(10, 10, anchor=NW, image=img2)

        # Right Side


window.mainloop()
