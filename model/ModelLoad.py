import os

import torch
from modelscope import pipelines
from modelscope.utils.constant import Tasks
import numpy as np
import cv2
import math

from common import ConstantDict


# scripts for crop images
def crop_image(img, position):
    def distance(x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

    position = position.tolist()
    for i in range(4):
        for j in range(i + 1, 4):
            if (position[i][0] > position[j][0]):
                tmp = position[j]
                position[j] = position[i]
                position[i] = tmp
    if position[0][1] > position[1][1]:
        tmp = position[0]
        position[0] = position[1]
        position[1] = tmp

    if position[2][1] > position[3][1]:
        tmp = position[2]
        position[2] = position[3]
        position[3] = tmp

    x1, y1 = position[0][0], position[0][1]
    x2, y2 = position[2][0], position[2][1]
    x3, y3 = position[3][0], position[3][1]
    x4, y4 = position[1][0], position[1][1]

    corners = np.zeros((4, 2), np.float32)
    corners[0] = [x1, y1]
    corners[1] = [x2, y2]
    corners[2] = [x4, y4]
    corners[3] = [x3, y3]

    img_width = distance((x1 + x4) / 2, (y1 + y4) / 2, (x2 + x3) / 2, (y2 + y3) / 2)
    img_height = distance((x1 + x2) / 2, (y1 + y2) / 2, (x4 + x3) / 2, (y4 + y3) / 2)

    corners_trans = np.zeros((4, 2), np.float32)
    corners_trans[0] = [0, 0]
    corners_trans[1] = [img_width - 1, 0]
    corners_trans[2] = [0, img_height - 1]
    corners_trans[3] = [img_width - 1, img_height - 1]

    transform = cv2.getPerspectiveTransform(corners, corners_trans)
    dst = cv2.warpPerspective(img, transform, (int(img_width), int(img_height)))
    return dst


def order_point(coor):
    arr = np.array(coor).reshape([4, 2])
    sum_ = np.sum(arr, 0)
    centroid = sum_ / arr.shape[0]
    theta = np.arctan2(arr[:, 1] - centroid[1], arr[:, 0] - centroid[0])
    sort_points = arr[np.argsort(theta)]
    sort_points = sort_points.reshape([4, -1])
    if sort_points[0][0] > centroid[0]:
        sort_points = np.concatenate([sort_points[3:], sort_points[:3]])
    sort_points = sort_points.reshape([4, 2]).astype('float32')
    return sort_points


def model_load():
    # ocr_detection = pipeline(Tasks.ocr_detection, model='./detection')
    ocr_recognition = pipelines.pipeline(Tasks.ocr_recognition, model='./recognition')
    img_dir = 'img'
    img_name = '21110003701.jpg'
    img_path = img_dir + '/' + img_name

    # img_path = '21110000901.jpg'

    image_full = cv2.imread(img_path)
    # det_result = ocr_detection(image_full)
    # det_result = det_result['polygons']
    det_result = [[10, 95, 1070, 95, 1070, 155, 10, 155], [10, 150, 1070, 150, 1070, 210, 10, 210],
                  [10, 205, 1070, 205, 1070, 265, 10, 265], [10, 260, 1070, 260, 1070, 320, 10, 320],
                  [10, 315, 1070, 315, 1070, 375, 10, 375], [10, 370, 1070, 370, 1070, 430, 10, 430],
                  [10, 425, 1070, 425, 1070, 485, 10, 485], [10, 480, 1070, 480, 1070, 540, 10, 540],
                  [10, 535, 1070, 535, 1070, 595, 10, 595], [10, 590, 1070, 590, 1070, 650, 10, 650],
                  [10, 645, 1070, 645, 1070, 705, 10, 705], [10, 700, 1070, 700, 1070, 760, 10, 760]]
    str = ''
    # print(det_result)

    # for i in range(det_result.shape[0]):
    for i in range(len(det_result)):
        pts = order_point(det_result[i])
        image_crop = crop_image(image_full, pts)
        result = ocr_recognition(image_crop)
        print(result)
        # str = result['text'][0] + str
    #     str = str + result['text'][0]
    # print(str)


def load_model(model_config_dict):
    model_name=model_config_dict['model_name']
    model=ConstantDict.Load_Model_dict.from_name(model_name)
    return model

def load_model_wts(model,model_config_dict):
    model_wts_path=model_config_dict['model_wight_path']
    model.load_state_dict(torch.load(model_wts_path))
    return model
def ocr_recognition_model_line_inference(model,crop_image):
    #single line ocr recognition
    result = model(crop_image)
    return result


def ocr_recognition_model_inference(ocr_detection_result,model,image):
    print("single image ocr recognition start")
    single_image_result=''
    for i in range(len(ocr_detection_result)):
        pts = order_point(ocr_detection_result[i])
        image_crop = crop_image(image, pts)
        result = ocr_recognition_model_line_inference(model,image_crop)
        single_image_result+=result['text'][0]+'\n'
        print(result)
    print("single image ocr recognition end")
    #utf8_bytes = single_image_result.encode('utf-8')
    return single_image_result




def ocr_detection_model_inference(model,image):
    print("single image ocr detection")
    det_result = [[10, 95, 1070, 95, 1070, 155, 10, 155], [10, 150, 1070, 150, 1070, 210, 10, 210],
                  [10, 205, 1070, 205, 1070, 265, 10, 265], [10, 260, 1070, 260, 1070, 320, 10, 320],
                  [10, 315, 1070, 315, 1070, 375, 10, 375], [10, 370, 1070, 370, 1070, 430, 10, 430],
                  [10, 425, 1070, 425, 1070, 485, 10, 485], [10, 480, 1070, 480, 1070, 540, 10, 540],
                  [10, 535, 1070, 535, 1070, 595, 10, 595], [10, 590, 1070, 590, 1070, 650, 10, 650],
                  [10, 645, 1070, 645, 1070, 705, 10, 705], [10, 700, 1070, 700, 1070, 760, 10, 760]]
    return det_result



def draw_table(list):
    list_img = cv2.imread(img_path)
    # point_list = []
    for i in range(len(list)):
        point_arr = np.array([[list[i][0], list[i][1]], [list[i][2], list[i][3]], [list[i][4], list[i][5]],
                              [list[i][6], list[i][7]]], np.int32).reshape((-1, 1, 2))
        cv2.polylines(list_img, [point_arr], True, (0, 255, 0), 3)
    # print(point_list)
    # point_list = np.array(point_list,np.int32).reshape((-1, 1, 2))
    # cv2.polylines(list_img, point_list, True, (0, 255, 0), 5)
    cv2.imwrite(img_dir + '/' + 'list' + img_name, list_img)

# draw_table(det_result)

#
# import jieba
#
# def compare_sentences(sentence1, sentence2):
#     # 使用 jieba 进行分词
#     words_set1 = set(jieba.cut(sentence1))
#     words_set2 = set(jieba.cut(sentence2))
#
#     # 比较不同点
#     diff1 = words_set1 - words_set2
#     diff2 = words_set2 - words_set1
#
#     return diff1, diff2
#
# import pandas as pd
# df = pd.read_csv('./pic/metadata.csv')
# # print(df)
# num = 0
# for i in range(1,100):
#     if ocr_recognition(cv2.imread('./pic/'+df.file_name[i]))['text'][0] != df['text'][i]:
#         num += 1
#         print(df.file_name[i])
#         print(ocr_recognition(cv2.imread('./pic/'+df.file_name[i]))['text'][0])
#         print(df['text'][i])
#         print(compare_sentences(ocr_recognition(cv2.imread('./pic/'+df.file_name[i]))['text'][0], df['text'][i]))
# print(num)
