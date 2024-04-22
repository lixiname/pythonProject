import os
import time
import tkinter
from tkinter import Frame, messagebox, Button, Label, StringVar
from tkinter.ttk import Combobox, Progressbar

from common.DefaultConfigPath import Load_resource_dict
from common.JsonReader import LogRuntimeJson
from common.TimesFormat import generate_time_stamp
from common.observerPattern import Observer, Observable
from component.ComboboxFrameComponent import ComboboxLoadFrame
from component.ImageFrameComponent import MarkImageFrame
from component.ListboxFrameComponent import ListboxFrame, ListboxMergeListFrame
from component.PathFrameComponent import PathLoadFrame, PathLoadNoButtonFrame
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
        task_list=self.taskListbox.merge_task_lists()
        all_image_list=self.listbox.get_list()
        all_image_dict={}
        for item in all_image_list:
            image_name=os.path.basename(item.rstrip('/'))
            all_image_dict[image_name]=item
        for item in task_list:
            self.task_list_path.append(all_image_dict[item])


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

    def get_model_name(self):
        return self.combobox.get_current_model_name()

    def get_model_ready(self):
        if not self.model_path:
            return False
        else:
            return True


class InferenceTaskPage3(Frame,Observable):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        Observable.__init__(self)
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

        self.progressbar['value'] = 0
        self.progressbar.pack(side='left')

        self.progressbar_label_bind = StringVar()

        self.progressbar_label = Label(self.frame_progressbar, width=20, height=1, textvariable=self.progressbar_label_bind)
        self.progressbar_label.pack(side='right')

        self.output_path_load()
        #控制任务是否暂停
        self.run_status=False
        self.task_next_input_index = 0
        self.task_image_list=[]
        self.model_path=None
        self.model_name=None

    def update_progressbar(self,current_item):
        self.frame_bottom.update()
        self.progressbar['value'] = current_item
        time.sleep(1)


    def start_or_pause_task(self):
        self.output_path_load()
        if self.task_button_status == 'start':
            if self.get_task_output_ready():
                self.run_status=True
                self.task_button_status = 'running'
                self.button_var_bind.set('执行中，点击则暂停')
                self.task_start()

            else:
                messagebox.showinfo('提示', "未设置输出路径")


        elif self.task_button_status == 'pause':
            if self.get_task_output_ready():
                self.run_status = True
                self.task_button_status = 'running'
                self.button_var_bind.set('执行中，点击则暂停')
                self.task_run()
            else:
                messagebox.showinfo('提示', "未设置输出路径")


        elif self.task_button_status == 'running':
            self.run_status = False
            self.task_button_status = 'pause'
            self.button_var_bind.set('已暂停，点击则继续执行')
            #arg = ['__', 'continue']




    def output_path_load(self):
        self.output_path =self.pathOutputFrame.get_path()
    def get_task_output_ready(self):
        if not self.output_path:
            return False
        else:
            return True

    def config_task_env(self,task_image_list,model_config_dict):
        self.task_image_list=task_image_list
        self.model_path =model_config_dict['model_path']
        self.model_name=model_config_dict['model_name']
        self.progressbar['maximum'] = len(self.task_image_list)
        self.progressbar_label_bind.set('0/' + str(len(self.task_image_list)))


    def task_start(self):
        self.load_model()
        self.task_run()

    def load_model(self):
        self.model_path

    def task_run(self):
        end=len(self.task_image_list)
        for i in range(self.task_next_input_index,end):
            if self.run_status==True:

                input_image_path=self.task_image_list[i]
                output=self.model_process(input_image_path)
                image_name=os.path.basename(input_image_path.rstrip('/'))
                out_file_name=image_name.split('.')[0]+'.txt'
                output_path=os.path.join(self.output_path,out_file_name)
                self.write_file(output_path,output)
                self.task_next_input_index += 1
                self.update_progressbar(i+1)
                self.progressbar_label_bind.set(str(i + 1) + '/' + str(len(self.task_image_list)))

                if i==end-1:
                    self.task_button.config(state=tkinter.DISABLED)
                    self.button_var_bind.set('已全部完成')



            else:
                break

    def write_file(self,output_path,output):
        with open(output_path,'w') as f:
            f.write(output)
            f.write('\n')


    def model_process(self,input_image_path):
        return input_image_path



    def logRuntimeJson(self):
        time_stamp = generate_time_stamp()
        model_name=self.model_name
        logJsonWriter=LogRuntimeJson(model_name,time_stamp)
        runtime_config_dict={}

        task_not_process_image_list = []
        end = len(self.task_image_list)
        for i in range(self.task_next_input_index, end):
            task_not_process_image_list.append(self.task_image_list[i])

        runtime_config_dict['task_not_process_image_list']=task_not_process_image_list
        runtime_config_dict['task_all_image_amount'] = end
        runtime_config_dict['model_path']=self.model_path
        runtime_config_dict['model_name'] = self.model_name
        runtime_config_dict['output_path'] = self.output_path
        logJsonWriter.logJson(runtime_config_dict)







class InferenceContinueTaskPage3(Frame,Observable):
    def __init__(self, parent,width,height):
        Frame.__init__(self, parent)
        Observable.__init__(self)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.title = Label(self.frame, width=20, height=1, text='选择中断的任务页面')
        self.title.pack(side='top')
        self.frame_extension = Frame(self.frame, width=width, height=1, bg='gold')
        self.frame_extension.pack(side='bottom')
        self.frame_bottom = Frame(self.frame, width=width, height=height, bg='lightgreen')
        self.frame_bottom.pack(side='bottom')

        self.combobox = ComboboxLoadFrame(self.frame_bottom)
        self.combobox.pack(side='top')

        # 任务继续部分
        self.button_var_bind = StringVar()
        self.button_var_bind.set('开始任务')
        self.task_button = Button(self.frame_bottom, textvariable=self.button_var_bind,
                                  command=lambda: self.start_or_pause_task())
        self.task_button.pack(side='bottom')
        self.task_button_status = 'start'

        self.frame_progressbar = Frame(self.frame_bottom, width=width, height=height, bg='lightgreen')
        self.frame_progressbar.pack(side='bottom')
        self.progressbar = Progressbar(self.frame_progressbar, orient=tkinter.HORIZONTAL, length=200,
                                       mode='determinate')

        self.progressbar['value'] = 0
        self.progressbar.pack(side='left')
        self.progressbar_label_bind = StringVar()
        self.progressbar_label = Label(self.frame_progressbar, width=20, height=1,
                                       textvariable=self.progressbar_label_bind)
        self.progressbar_label.pack(side='right')
        self.output_path_load()
        # 控制任务是否暂停
        self.run_status = False
        self.task_next_input_index = 0
        self.task_image_list = []
        self.model_path = None
        self.model_name = None

        # 详情
        self.frame_config = Frame(self.frame_bottom)
        self.frame_config.pack(side='bottom')
        # 左边栏
        self.frame_config_left = Frame(self.frame_config)
        self.frame_config_left.pack(side='left')
        self.frame_config_right = Frame(self.frame_config)
        self.frame_config_right.pack(side='right')

        self.frame_config_left_top = Frame(self.frame_config_left)
        self.frame_config_left_top.pack(side='top')
        self.output_path_text = PathLoadNoButtonFrame(self.frame_config_left_top, label="输出的位置")
        self.frame_config_left_bottom = Frame(self.frame_config_left)
        self.frame_config_left_bottom.pack(side='bottom')
        self.model_path_text = PathLoadNoButtonFrame(self.frame_config_left_bottom, label="选择的算法")

        self.textContent = TextContentFrame(self.frame_config_left)
        self.textContent.pack(side='bottom')


        #右边栏待处理图像列表
        self.frame_right_child_top = Frame(self.frame_config_right, width=width, height=height, bg='gold')
        self.frame_right_child_top.pack(side='top')
        self.frame_right_child_bottom = Frame(self.frame_config_right, width=width, height=height, bg='gold')
        self.frame_right_child_bottom.pack(side='bottom')

        self.frame_right_child_left = Frame(self.frame_right_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_left.pack(side='left')
        self.frame_right_child_right = Frame(self.frame_right_child_bottom, width=width, height=height, bg='gold')
        self.frame_right_child_right.pack(side='right')

        self.listbox = ListboxFrame(self.frame_right_child_right, width=width, height=int(height // 2))
        images_dir = Load_resource_dict.default_image_load_path()
        self.pathLoadFrame = PathLoadNoButtonFrame(self.frame_right_child_top, label="待识别图片列表")
        self.pathLoadFrame.addObserver(self.listbox)
        self.imageFrame = MarkImageFrame(self.frame_right_child_left)
        self.listbox.addObserver(self.imageFrame)
        #self.pathLoadFrame.notifyObservers(self.pathLoadFrame.get_path())


        self.combobox.addObserver(self.output_path_text)
        self.combobox.addObserver(self.model_path_text)
        self.combobox.addObserver(self.textContent)
        self.combobox.addObserver(self.pathLoadFrame)
        self.model_path = None
        self.combobox.init_default_model()



    def update_progressbar(self,current_item):
        self.frame_bottom.update()
        self.progressbar['value'] = current_item
        time.sleep(1)


    def start_or_pause_task(self):
        self.output_path_load()
        if self.task_button_status == 'start':
            if self.get_task_output_ready():
                self.run_status=True
                self.task_button_status = 'running'
                self.button_var_bind.set('执行中，点击则暂停')
                self.task_start()

            else:
                messagebox.showinfo('提示', "未设置输出路径")


        elif self.task_button_status == 'pause':
            if self.get_task_output_ready():
                self.run_status = True
                self.task_button_status = 'running'
                self.button_var_bind.set('执行中，点击则暂停')
                self.task_run()
            else:
                messagebox.showinfo('提示', "未设置输出路径")


        elif self.task_button_status == 'running':
            self.run_status = False
            self.task_button_status = 'pause'
            self.button_var_bind.set('已暂停，点击则继续执行')
            #arg = ['__', 'continue']


    def output_path_load(self):
        self.output_path =self.pathOutputFrame.get_path()
    def get_task_output_ready(self):
        if not self.output_path:
            return False
        else:
            return True

    def config_task_env(self,task_image_list,model_config_dict):
        self.task_image_list=task_image_list
        self.model_path =model_config_dict['model_path']
        self.model_name=model_config_dict['model_name']
        self.progressbar['maximum'] = len(self.task_image_list)
        self.progressbar_label_bind.set('0/' + str(len(self.task_image_list)))


    def task_start(self):
        self.load_model()
        self.task_run()

    def load_model(self):
        self.model_path

    def task_run(self):
        end=len(self.task_image_list)
        for i in range(self.task_next_input_index,end):
            if self.run_status==True:

                input_image_path=self.task_image_list[i]
                output=self.model_process(input_image_path)
                image_name=os.path.basename(input_image_path.rstrip('/'))
                out_file_name=image_name.split('.')[0]+'.txt'
                output_path=os.path.join(self.output_path,out_file_name)
                self.write_file(output_path,output)
                self.task_next_input_index += 1
                self.update_progressbar(i+1)
                self.progressbar_label_bind.set(str(i + 1) + '/' + str(len(self.task_image_list)))

                if i==end-1:
                    self.task_button.config(state=tkinter.DISABLED)
                    self.button_var_bind.set('已全部完成')



            else:
                break

    def write_file(self,output_path,output):
        with open(output_path,'w') as f:
            f.write(output)
            f.write('\n')

    def model_process(self,input_image_path):
        return input_image_path

    def logRuntimeJson(self):
        time_stamp = generate_time_stamp()
        model_name=self.model_name
        logJsonWriter=LogRuntimeJson(model_name,time_stamp)
        runtime_config_dict={}

        task_not_process_image_list = []
        end = len(self.task_image_list)
        for i in range(self.task_next_input_index, end):
            task_not_process_image_list.append(self.task_image_list[i])

        runtime_config_dict['task_not_process_image_list']=task_not_process_image_list
        runtime_config_dict['task_all_image_amount'] = end
        runtime_config_dict['model_path']=self.model_path
        runtime_config_dict['model_name'] = self.model_name
        runtime_config_dict['output_path'] = self.output_path
        logJsonWriter.logJson(runtime_config_dict)




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


