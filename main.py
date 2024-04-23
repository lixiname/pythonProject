# This is a sample Python script.
import os
import tkinter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt

from common import NetState
from common.DefaultConfigPath import Load_resource_dict
from common.observerPattern import Observer
from component.ImageFrameComponent import ImageReadLabelFrame, MarkImageFrame
from component.ListboxFrameComponent import ListboxFrame
from component.MainFrameComponent import main_windows_demo
from component.PathFrameComponent import PathLoadFrame


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Page1BoxRectangle(Frame):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()
        #左右栏
        self.child_fr1 = Frame(self.frame, width=width / 4 * 2, height=height, bg='blue')
        self.child_fr1.grid(row=0, column=0)
        self.child_fr2 = Frame(self.frame, width=width / 4, height=height, bg='yellow')
        self.child_fr2.grid(row=0, column=2)

        self.listbox = ListboxFrame(self.child_fr2, width=width, height=int(height // 2))
        out_dir= Load_resource_dict.default_label_output_path()
        images_dir=Load_resource_dict.default_image_load_path()
        self.pathLoadFrame = PathLoadFrame(self.child_fr2, images_dir, text="原始image加载路径")
        self.pathLoadFrame.addObserver(self.listbox)
        self.pathSaveFrame = PathLoadFrame(self.child_fr2, out_dir, text="保存标注结果的路径")

        self.imageFrame = MarkImageFrame(self.child_fr1)
        self.listbox.addObserver(self.imageFrame)
        self.save_and_next_button = Button(self.child_fr2, text="保存",
                                  command=lambda: self.save("save_and_next"))
        self.save_and_next_button.pack()
        self.pathLoadFrame.notifyObservers(self.pathLoadFrame.get_path())
        #self.next_button = Button(self.child_fr2, text="不保存直接选下一个",command=lambda: self.save("next"))
        #self.next_button.pack()

    def save(self, saveFlage):
        if saveFlage == "save_and_next":
            image_rectangles, image_rectangle_name = self.imageFrame.get_image_info()
            path = os.path.join(self.pathSaveFrame.get_path(), image_rectangle_name)
            with open(path,'w') as f:
                for item in image_rectangles:
                    str_tuple = tuple(map(str, item))
                    result = ",".join(str_tuple)
                    f.write(result)
                    f.write('\n')
            messagebox.showinfo('提示', '格式label已成功导出')


class Page2ReadRectangle(Frame):
    def __init__(self, parent,width,height,textSize):
        Frame.__init__(self,parent)

        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.child_fr1 = Frame(self.frame, width=width / 4 * 2, height=height, bg='blue')
        self.child_fr1.grid(row=0, column=0)
        self.child_fr2 = Frame(self.frame, width=width / 4, height=height, bg='yellow')
        self.child_fr2.grid(row=0, column=2)

        self.listbox = ListboxFrame(self.child_fr2, width=width, height=int(height // 2))
        images_dir= Load_resource_dict.default_label_load_path()
        self.pathLoadFrame = PathLoadFrame(self.child_fr2, images_dir, text="label加载路径")
        self.pathLoadFrame.addObserver(self.listbox)
        self.imageFrame = ImageReadLabelFrame(self.child_fr1)
        self.listbox.addObserver(self.imageFrame)
        self.pathLoadFrame.notifyObservers(self.pathLoadFrame.get_path())


class main_windows(Frame):
    def __init__(self, parent=None,width=1000,height=550,bg='lightgreen',textSize=8):
        super().__init__(parent)
        self.pack()
        self.frame_top =Frame(self,width=width, height=height,bg=bg)
        #self.frame_top.configure(background='red')
        self.frame_top.pack()
        self.width=width
        self.height=height
        self.textSize=textSize
        # 两个按钮用于导航栏切换页面
        train_button = Button(self.frame_top, text="标注", command=lambda: self.change_frame('box_rectangle'))
        train_button.grid(row=0, column=1, columnspan=1, padx=10, pady=5, sticky='w')
        test_button = Button(self.frame_top, text="查看", command=lambda: self.change_frame('read_rectangle'))
        test_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky='w')
        self.frame_middle = Frame(self, width=width, height=height*3/4, bg='lightgreen')
        self.frame_middle.pack()
        self.readRectangle=None
        self.boxRectangle=Page1BoxRectangle(self.frame_middle,self.width,self.height*3/4)
    def change_frame(self,flag):
        if flag == 'box_rectangle':
            if self.readRectangle is not None:
                self.readRectangle.pack_forget()
            if self.boxRectangle is not None:
                self.boxRectangle.pack()
            else:
                self.boxRectangle=Page1BoxRectangle(self.frame_middle,self.width,self.height*3/4)

        elif flag == 'read_rectangle':
            if self.boxRectangle is not None:
                self.boxRectangle.pack_forget()
            if self.readRectangle is not None:
                self.readRectangle.pack()
            else:
                self.readRectangle=Page2ReadRectangle(self.frame_middle,self.width,self.height*3/4,textSize=self.textSize)



def open_windows():
    textSize=10
    top = main_windows(textSize=textSize)
    top.mainloop()

def open_windows_demo():

    textSize=10
    top = main_windows_demo(textSize=textSize)
    #top.pack()
    top.mainloop()





def test():
    x = [214, 280, 362, 349, 284, 231]
    y = [325, 290, 320, 347, 316, 346]
    # 创建一个新的图形
    plt.figure(figsize=(40, 10))
    # 绘制二维坐标
    plt.plot(x, y)
    plt.xlabel('X轴')
    plt.ylabel('Y轴')
    plt.title('二维坐标图')

    # 显示图形
    plt.show()





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    NetState.getSystemInitInformation()
    NetState.getMemoryAllocatedNowAndChangedSizePrint()
    NetState.printMemoryNowReserved()
    open_windows_demo()

    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
