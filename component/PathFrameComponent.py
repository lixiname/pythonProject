from tkinter import Frame, StringVar, Label, Button
from tkinter.filedialog import askdirectory

from common.observerPattern import Observable, Observer


class PathLoadFrame(Frame,Observable):
    def __init__(self, parent,default_dir,text="选择文件夹的目录",width=80,height=5):
        Frame.__init__(self,parent,width=width,height=height)
        Observable.__init__(self)
        self.pack()
        self.path_bind = StringVar()
        self.path_bind.set(default_dir)
        self.path_text = Label(self, width=20, height=1, textvariable=self.path_bind)
        self.path_text.grid(row=0, column=0, columnspan=2, padx=10, pady=5, ipadx=150, sticky='e')
        self.path_button = Button(self, text=text,
                                 command=lambda: self.open_event_handler(self.path_bind))
        self.path_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky='w')

    def open_event_handler(self,bind):
        path = askdirectory()
        _path = path.replace("/", "\\")
        bind.set(_path)
        self.notifyObservers(_path)
    def get_path(self):
        return self.path_bind.get()



class PathLoadNoButtonFrame(Frame,Observer):
    def __init__(self, parent,label="选择文件夹的目录",width=80,height=5):
        Frame.__init__(self,parent,width=width,height=height)
        Observer.__init__(self)
        self.pack()
        self.path_label = Label(self, text=label)
        self.path_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5, sticky='w')
        self.path_bind = StringVar()
        self.path_bind.set("")
        self.path_text = Label(self, width=20, height=1, textvariable=self.path_bind)
        self.path_text.grid(row=0, column=2, columnspan=2, padx=10, pady=5, ipadx=150, sticky='e')

    def updates(self, arg):
        path=arg[1]
        self.path_bind.set(path)
