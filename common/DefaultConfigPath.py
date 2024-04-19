import os



class Load_resource_dict:
    @staticmethod
    def default_image_load_path():
        train_dir_path = os.path.join(os.getcwd(), "data", 'train_images')
        return train_dir_path

    @staticmethod
    def default_label_load_path():
        label_dir_path = os.path.join(os.getcwd(), "data", 'train_gts')
        return label_dir_path

    @staticmethod
    def default_label_output_path():
        label_dir_path = os.path.join(os.getcwd(), "data", 'train_out_gts')
        return label_dir_path

    @staticmethod
    def default_task_list_load_path():
        label_dir_path = os.path.join(os.getcwd(), "data", 'task_list')
        return label_dir_path

    @staticmethod
    def default_model_description_list_load_path():
        model_description_dir_path = os.path.join(os.getcwd(), "assert","description")
        return model_description_dir_path

    @staticmethod
    def default_model_list_load_path():
        model_dir_path = os.path.join(os.getcwd(), "assert", "model")
        return model_dir_path

