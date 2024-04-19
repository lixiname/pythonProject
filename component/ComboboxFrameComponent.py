import os
from tkinter import Frame, StringVar, Label, Button
from tkinter.filedialog import askdirectory
from tkinter.ttk import Combobox

from common.DefaultConfigPath import Load_resource_dict
from common.JsonReader import read_model_train_config
from common.observerPattern import Observable


class ComboboxLoadFrame(Frame,Observable):
    def __init__(self, parent,width=80,height=5):
        Frame.__init__(self,parent,width=width,height=height)
        Observable.__init__(self)
        self.pack()
        self.var_bind = StringVar()
        self.var_bind.set('模型1')
        self.combobox = Combobox(self,textvariable=self.var_bind)
        self.combobox.bind('<<ComboboxSelected>>', self.select_change)
        self.combobox['value'] = ('模型1', '模型2', '模型3')
        self.combobox.pack()
        self.model_description_dict = {'模型1': 'model1.txt', '模型2': 'model2.txt', '模型3': 'model3.txt'}
        self.model_dict = {'模型1': 'model1.txt', '模型2': 'model2.txt', '模型3': 'model3.txt'}

        self.description_dir = Load_resource_dict.default_model_description_list_load_path()
        self.model_dir = Load_resource_dict.default_model_list_load_path()
        self.model_description_path_list = os.listdir(self.description_dir)
        self.model_path_list = os.listdir(self.model_dir)
        self.current_model_path=None
        self.current_model_description_path=None

    def get_current_model_path(self):
        return self.current_model_path

    def select_change(self,event):
        self.change_model()
    def change_model(self):
        model_name = self.var_bind.get()

        model_file_name = self.model_dict[model_name]
        model_config_path = os.path.join(self.model_dir, model_file_name)
        json_content=read_model_train_config(model_config_path)
        self.current_model_path =json_content['model_path']

        file_name=self.model_description_dict[model_name]
        path=os.path.join(self.description_dir,file_name)
        self.current_model_description_path = path
        arg=['__',path]
        print('model_load_path')
        print(self.current_model_path)
        self.notifyObservers(arg)

    def init_default_model(self):
        self.change_model()

