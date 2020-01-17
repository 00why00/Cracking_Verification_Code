# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: predict.py
@ide: PyCharm
@time: 2020/1/1716:38
"""
import keras
from keras import models
import numpy as np
import string
from PIL import Image

model = models.load_model('cnn.h5')  # 模型加载
img_rows, img_cols = 12, 22
predict_output = []

character = string.ascii_lowercase + string.digits

if keras.backend.image_data_format == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)


def img_processing(image):
    # img = Image.open(filepath)
    im = image.point(lambda i: i != 43, mode='1')
    y_min, y_max = 0, 22
    split_lines = [5, 17, 29, 41, 53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    return ims


def predict_images(images):
    for image_index in range(4):
        img = images[image_index]
        predict_input = 1.0 * np.array(img)
        predict_input = predict_input.reshape(1, *input_shape)
        y = model.predict(predict_input)
        y_char = character[np.argmax(y)]
        predict_output.append(y_char)
    return ''.join(predict_output)


def predict(image):
    return predict_images(img_processing(image))
