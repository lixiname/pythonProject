import os
from tkinter import Frame, StringVar, Label, Button, Listbox
from tkinter.constants import END
from tkinter.filedialog import askdirectory

from common.observerPattern import Observable, Observer


class ListboxFrame(Frame,Observer,Observable):
    def __init__(self, parent, width,height):
        Frame.__init__(self,parent,width=width,height=6)
        Observer.__init__(self)
        Observable.__init__(self)
        self.pack()
        self.dir=''
        self.listbox = Listbox(self, selectmode="single")
        self.listbox.bind("<Button-1>", lambda event: self.on_select(event, self.listbox))
        self.listbox.config(width=20,height=6)
        self.listbox.insert(0, "占位lists[item]")
        self.listbox.insert(1, "占位lists[item]")
        self.listbox.insert(2, "占位lists[item]")
        self.listbox.grid(row=0,column=0)
        self.curselection = 0
        self.lists=[]
    def on_select(self,event,listbox):
        if len(listbox.curselection())==1:
            self.curselection = listbox.curselection()[0]
            item = listbox.get(self.curselection)
            path=os.path.join(self.dir,item)
            arg = ['__', path]
            Observable.notifyObservers(self,arg)
    def task(self):
        num=0
        for item in range(self.listbox.size()):
            path=os.path.join(self.dir,self.listbox.get(item))
            arg=['task',path]
            Observable.notifyObservers(self, arg)
            num +=1
        return num

    def updates(self,arg):
        self.listbox.delete(0,END)
        self.lists=os.listdir(arg)
        self.dir=arg
        for item in range(len(self.lists)):
            #(index,item_path)
            self.listbox.insert(item,self.lists[item])
        print('------list refrash complete------')

    def get_current_element(self):
        self.listbox.curselection()

    def get_list(self):
        return self.lists




class ListboxMergeListFrame(ListboxFrame):
    def __init__(self, parent, width,height):
        ListboxFrame.__init__(self,parent,width=width,height=6)
        self.pack()

    def merge_task_lists(self):
        task_list=[]
        for file_name in self.lists:
            path = os.path.join(self.dir, file_name)
            with open(path, 'r') as f:
                while True:
                    line = f.readline().rstrip()
                    if not line:
                        break
                    task_list.append(line)
        print("task_merge list start")
        for item in task_list:
            print(item)
        print("task_merge list end")
        return task_list



