import tkinter
from tkinter import Frame, Button, messagebox, StringVar, Label, Radiobutton, IntVar

from common.DefaultConfigPath import Load_resource_dict
from common.observerPattern import Observable, Observer
from component.ImageFrameComponent import ImageReadLabelFrame
from component.ListboxFrameComponent import ListboxFrame
from component.PageFrameCommponent import InferenceTaskPage1, InferenceContinueTaskPage1, InferenceTaskPage2, \
    InferenceTaskPage3, InferenceTaskPage4
from component.PathFrameComponent import PathLoadFrame


class InferenceMainContainPage(Frame,Observer):
    def __init__(self, parent,width,height):
        Frame.__init__(self,parent)
        Observer.__init__(self)
        self.pack(anchor='center',fill='y')
        self.frame = Frame(self, width=width, height=height, bg='green')
        self.frame.pack()
        self.width=width
        self.height = height
        self.contain=InferenceTaskSelectPage(self.frame,width,height)
        self.contain.addObserver(self)


    def updates(self, arg):
        flag=arg[1]
        if flag == 'start_new':
            #销毁old窗口
            self.contain.pack_forget()
            self.contain = InferenceNewTaskContainPage(self.frame,self.width,self.height)
        elif flag == 'continue_before':
            self.contain = InferenceContinueTaskPage1(self.frame,self.width,self.height)



class InferenceTaskSelectPage(Frame,Observable):
    def __init__(self, parent,width,height):
        Frame.__init__(self,parent)
        Observable.__init__(self)
        self.pack()
        self.frame = Frame(self, width=width, height=height/4, bg='lightgreen')
        self.frame.pack()
        self.frame_expansive = Frame(self, width=width, height=height/4, bg='lightgreen')
        self.frame_expansive.pack()
        self.start_new_button = Button(self.frame, text="开始新任务", command=lambda: self.change_frame('start_new'))
        self.start_new_button.grid(row=0, column=1, columnspan=1, padx=10, pady=5, sticky='w')
        self.continue_before_button = Button(self.frame, text="选择已有的未处理完的任务", command=lambda: self.change_frame('continue_before'))
        self.continue_before_button.grid(row=0, column=3, columnspan=1, padx=10, pady=5, sticky='w')

    def change_frame(self,flag):
        arg = ['__', flag]
        self.notifyObservers(arg)


class InferenceNewTaskContainPage(Frame, Observable):
    def __init__(self, parent, width, height):
        Frame.__init__(self, parent)
        Observable.__init__(self)
        self.pack()
        self.frame_bottom = Frame(self, width=width, height=height)
        self.frame_bottom.pack(fill='x',side='bottom')
        self.width = width
        self.height = height

        self.frame_expansive = Frame(self, width=width, height=2, bg='lightgreen')
        self.frame_expansive.pack()


        self.pre_button = Button(self.frame_bottom, text="上一步", command=lambda: self.change_frame('pre'))
        self.next_button = Button(self.frame_bottom, text="下一步",
                                        command=lambda: self.change_frame('next'))
        self.next_button.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky='w')

        self.frame_middle = Frame(self, width=width, height=height * 3 / 4, bg='lightgreen')
        self.frame_middle.pack()
        self.frame_process = Frame(self, width=width, bg='lightgreen')
        self.frame_process.pack(fill='x')
        self.current_status = 1
        self.start_new_list_management = {}
        self.continue_before_list_management = []

        page = InferenceTaskPage1(self.frame_middle, self.width, self.height * 3 / 4)
        self.start_new_list_management['page1']=page
        self.start_new_list_management['page1'].pack()

        #进度管理
        self.radiobutton_list_management = {}
        self.radio_value_list = {}
        radio_text = ["输入数据", "选择模型", "选择输出位置", "查看结果"]
        self.radio_label_text = {}

        self.radio_label_list = {}

        for i in range(1, 5):
            self.radio_value_list[f'page{i}'] = IntVar()
            self.radio_value_list[f'page{i}'].set(0)
            self.radiobutton_list_management[f'page{i}'] = \
                Radiobutton(self.frame_process, text=radio_text[i - 1], variable=self.radio_value_list[f'page{i}'],
                            value=1,compound='left')
            self.radiobutton_list_management[f'page{i}'].config(state=tkinter.DISABLED)
            self.radiobutton_list_management[f'page{i}'].grid(column=i,row=1,rowspan=2)

            self.radio_label_text[f'page{i}'] = StringVar()
            self.radio_label_text[f'page{i}'].set("")
            self.radio_label_list[f'page{i}'] = Label(self.frame_process, width=20, height=1, textvariable=self.radio_label_text[f'page{i}'])
            self.radio_label_list[f'page{i}'].grid(column=i, row=0)

        self.radio_value_list[f'page{self.current_status}'].set(1)
        self.radio_label_text[f'page{self.current_status}'].set("当前")
        self.radio_label_text[f'page{self.current_status+1}'].set("下一步")

    def change_frame(self, flag):
        if flag == 'pre':
            self.start_new_list_management[f'page{self.current_status}'].pack_forget()
            self.start_new_list_management[f'page{self.current_status - 1}'].pack()
            self.change_radio_status('pre')
            self.change_radio_label_text('pre')
            self.current_status -= 1


        elif flag == 'next':
            (ready,message)=self.check_current_status_ready()
            if ready:
                self.change_radio_status('next')
                self.change_radio_label_text('next')
                self.start_new_list_management[f'page{self.current_status}'].pack_forget()
                if self.exist(f"page{self.current_status + 1}"):

                    self.start_new_list_management[f'page{self.current_status + 1}'].pack()
                    if self.current_status + 1 == 3:
                        task_lists = self.start_new_list_management[f'page{self.current_status - 1}'].get_task_lists()
                        model_path = self.start_new_list_management[f'page{self.current_status }'].model_path_load()
                        self.start_new_list_management[f'page{self.current_status + 1}'].config_task_env(task_lists, model_path)
                else:
                    (page_key, page) = self.create_page(self.current_status + 1)
                    self.start_new_list_management[page_key] = page
                self.current_status += 1
                #messagebox.showinfo('提示', message)
                print('info:'+message)
                print("next process")
            else:
                messagebox.showinfo('提示', message)
                print("current must require things status not ready")


        self.button_state()

    def exist(self,page_key):
        if page_key in self.start_new_list_management:
            return True
        else:
            return False
    def create_page(self,page):
        if page==2:
            new_page = InferenceTaskPage2(self.frame_middle, self.width, self.height * 3 / 4)
        elif page==3:
            new_page = InferenceTaskPage3(self.frame_middle, self.width, self.height * 3 / 4)
            task_lists=self.start_new_list_management['page1'].get_task_lists()
            model_path=self.start_new_list_management['page2'].model_path_load()
            new_page.config_task_env(task_lists, model_path)
        elif page==4:
            new_page = InferenceTaskPage4(self.frame_middle, self.width, self.height * 3 / 4)
        page_key=f'page{page}'
        return (page_key,new_page)

    def button_state(self):
        if self.current_status == 1:
            self.pre_button.grid_forget()
        else:
            self.pre_button.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        if self.current_status==4:
            self.next_button.grid_forget()
        else:
            self.next_button.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky='w')

    def change_radio_status(self,flag):
        if flag=='pre':
            self.radio_value_list[f'page{self.current_status}'].set(0)
        elif flag=='next':
            self.radio_value_list[f'page{self.current_status+1}'].set(1)


    def change_radio_label_text(self,flag):
        if flag=='pre':
            self.radio_label_text[f'page{self.current_status - 1}'].set("当前")
            self.radio_label_text[f'page{self.current_status}'].set("下一步")
            if self.current_status + 1<5:
                self.radio_label_text[f'page{self.current_status + 1}'].set("")

        elif flag=='next':
            self.radio_label_text[f'page{self.current_status}'].set("")
            self.radio_label_text[f'page{self.current_status + 1}'].set("当前")
            if self.current_status + 2<5:
                self.radio_label_text[f'page{self.current_status + 2}'].set("下一步")

    def check_current_status_ready(self):
        if self.current_status == 1:
            self.start_new_list_management[f'page{self.current_status}'].merge_task_lists()
            ready=self.start_new_list_management[f'page{self.current_status}'].get_task_list_ready()
            if ready:
                return (True,"当前步骤内容完成")
            else:
                return (False,"任务清单为空")
        elif self.current_status == 2:
            self.start_new_list_management[f'page{self.current_status}'].model_path_load()
            ready=self.start_new_list_management[f'page{self.current_status}'].get_model_ready()
            if ready:
                return (True,"当前步骤内容完成")
            else:
                return (False,"请选择算法")
        elif self.current_status == 3:
            self.start_new_list_management[f'page{self.current_status}'].output_path_load()
            ready=self.start_new_list_management[f'page{self.current_status}'].get_task_output_ready()

            if ready:
                return (True,"已暂停任务")
            else:
                return (False,"输出位置不能为空")


class TrainMainContainPage(Frame):
    def __init__(self, parent,width,height):
        Frame.__init__(self,parent)
        self.pack()
        self.frame = Frame(self, width=width, height=height, bg='lightgreen')
        self.frame.pack()

        self.title = Label(self.frame, width=20, text='训练主页面')
        self.title.pack(side='top')
        self.frame_extension = Frame(self.frame, width=width, height=1, bg='gold')
        self.frame_extension.pack(side='bottom')
        self.content = Label(self.frame, width=20, text='待定')
        self.content.pack(side='bottom')
