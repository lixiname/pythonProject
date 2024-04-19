import os
from tkinter import Frame, StringVar, Label, Button, Listbox, Canvas
from tkinter.constants import END, NW
from tkinter.filedialog import askdirectory
from PIL import Image
import cv2
from PIL import ImageTk

from common.observerPattern import Observable, Observer



class TextContentFrame(Frame, Observer, Observable):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Observer.__init__(self)
        Observable.__init__(self)
        self.pack()
        self.bindContent=StringVar()
        self.textContent = Label(self,textvariable=self.bindContent)
        self.textContent.pack()

    def updates(self, arg):
        path= arg[1]
        content=""
        with open(path, 'r',encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                content+=line
        print("model description content")
        print(content)
        self.bindContent.set(content)

    def get_content_info(self):
        return self.bindContent.get()