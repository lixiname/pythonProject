import json
import os

def read_model_train_config(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data