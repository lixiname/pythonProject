import os
import time
import tkinter
from tkinter import Frame, messagebox, Button, Label, StringVar
from tkinter.ttk import Combobox, Progressbar

from common.DefaultConfigPath import Load_resource_dict
from common.observerPattern import Observer
from component.ComboboxFrameComponent import ComboboxLoadFrame
from component.ImageFrameComponent import MarkImageFrame
from component.ListboxFrameComponent import ListboxFrame, ListboxMergeListFrame
from component.PathFrameComponent import PathLoadFrame
from component.TextFrameComponent import TextContentFrame


class InferenceTaskPage1(Frame,Observer):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        Observer.__init__(self)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()


        #选择模型,选择输出位置,查看结果

        self.title = Label(self.frame, width=20, height=1, text='数据选择页面')
        self.title.pack(side='top')
        # 左右栏
        self.frame_left = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_left.pack(side='left')

        self.frame_left_child_top = Frame(self.frame_left, width=width, height=height, bg='gold')
        self.frame_left_child_top.pack(side='top')
        self.frame_left_child_bottom = Frame(self.frame_left, width=width, height=height, bg='gold')
        self.frame_left_child_bottom.pack(side='bottom')

        self.frame_left_child_left = Frame(self.frame_left_child_bottom, width=width, height=height, bg='gold')
        self.frame_left_child_left.pack(side='left')
        self.frame_left_child_right = Frame(self.frame_left_child_bottom, width=width, height=height, bg='gold')
        self.frame_left_child_right.pack(side='right')

        self.listbox = ListboxFrame(self.frame_left_child_right, width=width, height=int(height // 2))
        images_dir = Load_resource_dict.default_image_load_path()
        self.pathLoadFrame = PathLoadFrame(self.frame_left_child_top, images_dir, text="原始image加载路径")
        self.pathLoadFrame.addObserver(self.listbox)
        self.imageFrame = MarkImageFrame(self.frame_left_child_left)
        self.listbox.addObserver(self.imageFrame)
        self.pathLoadFrame.notifyObservers(self.pathLoadFrame.get_path())

        # 左右栏
        self.frame_right = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_right.pack(side='right')

        self.frame_right_child_top = Frame(self.frame_right, width=width, height=height, bg='gold')
        self.frame_right_child_top.pack(side='top')
        self.frame_right_child_bottom = Frame(self.frame_right, width=width, height=height, bg='gold')
        self.frame_right_child_bottom.pack(side='bottom')

        self.frame_right_child_left = Frame(self.frame_right_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_left.pack(side='left')
        self.frame_right_child_right = Frame(self.frame_right_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_right.pack(side='right')

        self.taskListbox = ListboxMergeListFrame(self.frame_right_child_right, width=width, height=int(height // 2))

        task_dir=Load_resource_dict.default_task_list_load_path()
        self.taskPathLoadFrame = PathLoadFrame(self.frame_right_child_top, task_dir, text="加载需要处理的图片清单文件目录")
        self.taskPathLoadFrame.addObserver(self.taskListbox)
        self.textContentFrame = TextContentFrame(self.frame_right_child_left)
        self.taskListbox.addObserver(self.textContentFrame)
        self.taskPathLoadFrame.notifyObservers(self.taskPathLoadFrame.get_path())
        self.task_list_path=[]

    def updates(self, arg):
        path_list= arg[1]

    def merge_task_lists(self):
        self.task_list_path=self.taskListbox.merge_task_lists()

    def get_task_lists(self):
        return self.task_list_path

    def get_task_list_ready(self):
        if not self.task_list_path:
            return False
        else:
            return True





class InferenceTaskPage2(Frame):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.title = Label(self.frame, width=20, height=1, text='模型选择页面')
        self.title.pack(side='top')
        self.frame_extension = Frame(self.frame, width=width, height=1, bg='gold')
        self.frame_extension.pack(side='bottom')
        self.frame_bottom = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_bottom.pack(side='bottom')

        self.combobox = ComboboxLoadFrame(self.frame_bottom)
        self.combobox.pack(side='top')
        self.textContent = TextContentFrame(self.frame_bottom)
        self.textContent.pack(side='bottom')
        self.combobox.addObserver(self.textContent)
        self.model_path=None
        self.combobox.init_default_model()


    def model_path_load(self):
        self.model_path =self.combobox.get_current_model_path()

    def get_model_path(self):
        return self.model_path
    def get_model_ready(self):
        if not self.model_path:
            return False
        else:
            return True


class InferenceTaskPage3(Frame):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.title = Label(self.frame, width=20, height=1, text='输出选择页面')
        self.title.pack(side='top')
        self.frame_extension = Frame(self.frame, width=width, height=1, bg='gold')
        self.frame_extension.pack(side='bottom')
        self.frame_bottom = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_bottom.pack(side='bottom')

        out_dir = Load_resource_dict.default_label_output_path()
        self.pathOutputFrame = PathLoadFrame(self.frame_bottom, out_dir, text="检测输出目录路径")

        self.button_var_bind = StringVar()
        self.button_var_bind.set('开始任务')
        self.task_button = Button(self.frame_bottom, textvariable=self.button_var_bind, command=lambda: self.start_or_pause_task())
        self.task_button.pack(side='bottom')
        self.task_button_status = 'start'
        self.output_path=None

        self.frame_progressbar = Frame(self.frame_bottom, width=width, height=height, bg='lightgreen')
        self.frame_progressbar.pack(side='bottom')
        self.progressbar=Progressbar(self.frame_progressbar, orient=tkinter.HORIZONTAL, length=200, mode='determinate')
        self.progressbar['maximum'] = 100
        self.progressbar['value'] = 0
        self.progressbar.pack(side='left')

        self.path_bind = StringVar()
        self.path_bind.set()
        self.path_text = Label(self, width=20, height=1, textvariable=self.path_bind)


        self.progressbar_label = Label(self.frame_progressbar,)
        self.progressbar_label.pack(side='right')

    def update_progressbar(self):
        for item in range(100):
            self.frame_bottom.update()
            self.progressbar['value'] = item

            print('')
            time.sleep(0.05)


    def start_or_pause_task(self):
        if self.task_button_status == 'start':
            self.task_button_status = 'running'
            self.button_var_bind.set('执行中，点击则暂停')
            self.update_progressbar()

        elif self.task_button_status == 'pause':
            self.task_button_status = 'running'
            self.button_var_bind.set('执行中，点击则暂停')
            self.update_progressbar()

        elif self.task_button_status == 'running':
            self.task_button_status = 'pause'
            self.button_var_bind.set('已暂停，点击则继续执行')



    def output_path_load(self):
        self.output_path =self.pathOutputFrame.get_path()
    def get_task_output_ready(self):
        if not self.output_path:
            return False
        else:
            return True





class InferenceTaskPage4(Frame):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.title = Label(self.frame, width=20, height=1, text='结果查看页面')
        self.title.pack(side='top')
        self.frame_extension = Frame(self.frame, width=width, height=1, bg='gold')
        self.frame_extension.pack(side='bottom')
        self.frame_bottom = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_bottom.pack(side='bottom')

        # 左右栏

        self.frame_bottom_child_top = Frame(self.frame_bottom, width=width, height=height, bg='gold')
        self.frame_bottom_child_top.pack(side='top')
        out_dir = Load_resource_dict.default_label_output_path()
        self.taskPathLoadFrame = PathLoadFrame(self.frame_bottom_child_top, out_dir,text="结果目录")

        self.frame_bottom_child_bottom = Frame(self.frame_bottom, width=width, height=height, bg='gold')
        self.frame_bottom_child_bottom.pack(side='bottom')

        self.frame_right_child_left = Frame(self.frame_bottom_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_left.pack(side='left')
        self.frame_right_child_right = Frame(self.frame_bottom_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_right.pack(side='right')

        self.taskListbox = ListboxMergeListFrame(self.frame_right_child_right, width=width, height=int(height // 2))

        self.taskPathLoadFrame.addObserver(self.taskListbox)
        self.textContentFrame = TextContentFrame(self.frame_right_child_left)
        self.taskListbox.addObserver(self.textContentFrame)
        self.taskPathLoadFrame.notifyObservers(self.taskPathLoadFrame.get_path())




class InferenceContinueTaskPage1(Frame):
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

