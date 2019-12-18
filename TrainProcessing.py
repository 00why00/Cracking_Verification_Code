# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: TrainProcessing.py
@ide: PyCharm
@time: 2019/12/18 15:26
"""
import ImageProcessing
from PIL import Image
import os


train_path = './train/'
character_path = './src/'
isExists=os.path.exists(character_path)
if not isExists:
    os.mkdir(character_path)

fileList = os.listdir(train_path)
for filename in fileList:
    processed_img = ImageProcessing.img_processing(train_path + filename)
    for i in range(4):
        processed_img[i].save('./src/{}_{}.gif'.format(fileList.index(filename), i))
