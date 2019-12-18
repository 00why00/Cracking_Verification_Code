# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: ImageProcessing.py
@ide: PyCharm
@time: 2019/12/18 14:06
"""
from PIL import Image, ImageFilter
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# 获取灰度转二值的映射table 0表示黑色,1表示白色
def get_bin_table():
    table = []
    for i in range(256):
        if i < 100:
            table.append(0)
        else:
            table.append(1)
    return table


# 验证码处理降噪+分割
def img_processing(img_path):
    # 转为灰度图像
    img = Image.open(img_path)
    img1 = img.convert("L")
    # img1.show()
    # 二值化
    table = get_bin_table()
    img2 = img1.point(table, "1")
    # img2.show()
    # 去除噪点
    img3 = img2.filter(ImageFilter.SMOOTH)
    # img3.show()
    # 图像切割
    y_min, y_max = 0, 22  # 去除下方空白
    split_lines = [5, 17, 29, 41, 53]
    img4 = [img3.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    # for i in range(4):
    #     plt.subplot(1, 4, i + 1)
    #     plt.imshow(img4[i], interpolation='none')
    # plt.show()
    return img4


if __name__ == '__main__':
    img_processing('./CheckCode.gif')