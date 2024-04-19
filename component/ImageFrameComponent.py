import os
from tkinter import Frame, StringVar, Label, Button, Listbox, Canvas
from tkinter.constants import END, NW
from tkinter.filedialog import askdirectory
from PIL import Image
import cv2
from PIL import ImageTk

from common.observerPattern import Observable, Observer

class MarkImageFrame(Frame, Observer, Observable):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Observer.__init__(self)
        Observable.__init__(self)
        self.pack()
        self.img_gif = None
        self.imageView = Label(self)
        self.imageView.pack()
        self.image_rectangles = []
        self.cvImage=None
        self.canvas=None
        self.save_rectangle_list=[]
    def updates(self, arg):
        infix='train_images'
        image_path = arg[1]
        file_name = os.path.basename(arg[1].rstrip('/'))
        #要适应多种后缀的图像文件格式 png、jpg等->txt
        label_name = file_name.split(".")[0]+'.txt'
        label_dir, filename = os.path.split(arg[1])
        image_prefix_dir, _ = os.path.split(label_dir)
        label_path = os.path.join(image_prefix_dir, infix, label_name)

        self.label_name = label_name
        self.cvImage = cv2.imread(image_path)

        # 创建画布
        height, width, channels = self.cvImage.shape
        if self.canvas is not None:
            self.canvas.destroy()
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
        # 绑定鼠标移动事件
        self.canvas.bind('<Button-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.init_draw_image()
        print()


    def get_image_info(self):
        return self.image_rectangles, self.label_name

    def pine_rectangle(self):
        (x1, y1, x3, y3)=(self.x1, self.y1, self.x3, self.y3)
        #cv2.rectangle(self.cvImage, (x1, y1), (x3, y3), (0, 255, 0), 1)
        (x2, y2, x4, y4)=(x3,y1,x1,y3)
        cls="-10"
        self.image_rectangles.append((x1, y1, x2, y2, x3, y3,x4, y4,cls))

    def init_draw_image(self):
        cv2image = cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)
        self.img_gif = ImageTk.PhotoImage(current_image)
        # 在画布上显示图像
        self.image_draw_id=self.canvas.create_image(0, 0, anchor=NW, image=self.img_gif)
        #self.imageView.img = img_gif
        #self.imageView.configure(image=img_gif)
        print("init image")

    def on_button_press(self, event):
        self.x1 = event.x
        self.y1 = event.y

    def on_move_press(self, event):
        height, width, channels = self.cvImage.shape
        x3 = min(event.x, width)
        y3 = min(event.y, height)
        self.delete_except_rectangle_list()
        self.canvas.create_rectangle(self.x1, self.y1, x3, y3, outline='red')


    def on_button_release(self, event):
        self.x3 = event.x
        self.y3 = event.y
        self.pine_rectangle()
        self.delete_except_rectangle_list()
        obj_id = self.canvas.create_rectangle(self.x1, self.y1, self.x3, self.y3, outline='red')
        self.save_rectangle_list.append(obj_id)

    def delete_except_rectangle_list(self):
        all_obj_id=self.canvas.find_all()
        for obj_id in all_obj_id:
            if obj_id!=self.image_draw_id:
                if obj_id not in self.save_rectangle_list:
                    self.canvas.delete(obj_id)



class ImageReadLabelFrame(Frame, Observer, Observable):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Observer.__init__(self)
        Observable.__init__(self)
        self.pack()
        self.image = None
        self.imageView = Label(self)
        self.imageView.pack()

    def updates(self, arg):
        infix='train_images'
        label_path = arg[1]
        file_name = os.path.basename(arg[1].rstrip('/'))
        #要适应多种后缀的文件格式
        image_name = file_name.replace('.txt', '.jpg')
        label_dir, filename = os.path.split(arg[1])
        image_prefix_dir, _ = os.path.split(label_dir)
        path = os.path.join(image_prefix_dir, infix, image_name)

        single_image_label = []
        with open(label_path, 'r') as f:
            while True:
                label_content = f.readline()
                if not label_content:
                    break
                content = label_content.replace('\n', ',-1')
                single_image_label.append([int(item) for item in content.split(',')])

        cvImage = cv2.imread(path)
        height, width, channels = cvImage.shape

        self.image_rectangles=[]
        #以左上角为起点,顺时针4个点坐标
        for item in single_image_label:
            x1, y1, x2, y2, x3, y3, x4, y4, cls, _ = item[0], item[1], item[2], item[3], item[4],item[5],item[6], item[7], item[8],item[9]
            cv2.rectangle(cvImage, (x1, y1), (x3, y3), (0, 255, 0), 1)
            self.image_rectangles.append((x1, y1, x2, y2, x3, y3, x4, y4, cls))

        cv2image = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)
        img_gif = ImageTk.PhotoImage(current_image)
        self.image_rectangle_name = file_name
        self.imageView.img = img_gif
        self.imageView.configure(image=img_gif)
        print("image load complete")

    def get_image_info(self):
        return self.image_rectangles, self.image_rectangle_name
