import os

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

class Load_Model_dict:
    @staticmethod
    def from_name(model_name):
        file_path = os.path.join(os.getcwd(), "assert", "recognition")
        print(f'wts_path- {file_path}')
        if model_name == "model1":
            ocr_recognition = pipeline(Tasks.ocr_recognition, model=file_path)
            return ocr_recognition
        elif model_name == "model2":
            ocr_recognition = pipeline(Tasks.ocr_recognition, model=file_path)
            return ocr_recognition
        elif model_name == "model3":
            ocr_recognition = pipeline(Tasks.ocr_recognition, model=file_path)
            return ocr_recognition
