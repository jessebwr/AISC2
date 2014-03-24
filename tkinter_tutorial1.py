#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

This script shows a simple window
on the screen.

author: Jan Bodnar
last modified: January 2011
website: www.zetcode.com
"""

from Tkinter import Tk, BOTH
from ttk import Frame, Button, Style

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
    def initUI(self):
      
        self.parent.title("Quit button")
        self.style = Style()
        self.style.theme_use("default")

        #Expand the frame to fill the parent window in both directions
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        
        #Create a quit button (Stops the program but does not close the window!)
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=50, y=50)
        
    def centerWindow(self):
      
        #The width and height of the window
        w = 290
        h = 150

        #Get the dimension of the screen
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        #The coordinates of the center of the screen
        x = (sw - w)/2
        y = (sh - h)/2
        
        #Initialize and center the root window
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        

def main():
    #Create the root window
    root = Tk()
    #Create an instance of the application class
    app = Example(root)
    #Enter the event handling loop
    root.mainloop()  


if __name__ == '__main__':
    main()  