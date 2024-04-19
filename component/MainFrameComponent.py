import tkinter
from tkinter import Frame, Button

from component.ContainFrameComponent import TrainMainContainPage, InferenceMainContainPage


class main_windows_demo(Frame):
    def __init__(self, parent=None,width=700,height=900,bg='black',textSize=8):
        super().__init__(parent,width=width,height=height)
        self.pack(padx=10,pady=10)
        self.frame_top =Frame(self,width=width/2,bg=bg)
        #self.frame_top.configure(background='red')
        self.frame_top.pack(fill=tkinter.Y,side=tkinter.LEFT)
        self.width=width
        self.height=height
        self.textSize=textSize
        # 两个按钮用于导航栏切换页面
        self.train_button = Button(self.frame_top, text="训练", command=lambda: self.change_frame('train'))
        self.train_button.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        self.test_button = Button(self.frame_top, text="推理", command=lambda: self.change_frame('inference'))
        self.test_button.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        self.frame_middle = Frame(self, width=width, height=height*3/4, bg='gold')
        self.frame_middle.pack(fill=tkinter.Y,side=tkinter.RIGHT,anchor='center')
        self.trainMainPage=None
        self.inferenceMainPage=InferenceMainContainPage(self.frame_middle,self.width,self.height*3/4)
    def change_frame(self,flag):
        if flag == 'train':
            if self.inferenceMainPage is not None:
                self.inferenceMainPage.pack_forget()
            if self.trainMainPage is not None:
                self.trainMainPage.pack()
            else:
                self.trainMainPage=TrainMainContainPage(self.frame_middle,self.width,self.height*3/4)

        elif flag == 'inference':
            if self.trainMainPage is not None:
                self.trainMainPage.pack_forget()
            if self.inferenceMainPage is not None:
                self.inferenceMainPage.pack()
            else:
                self.inferenceMainPage=InferenceMainContainPage(self.frame_middle,self.width,self.height*3/4)