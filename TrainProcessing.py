# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: TrainProcessing.py
@ide: PyCharm
@time: 2019/12/18 15:26
"""
# 进行训练前的处理
import ImageProcessing
from PIL import Image
import os

# 训练集路径
train_path = './train/'
# 拆分后的字符路径
character_path = './src/'
# 根据情况新建字符路径文件夹
isExists = os.path.exists(character_path)
if not isExists:
    os.mkdir(character_path)
# 得到训练集图片迭代器
fileList = os.listdir(train_path)
# 将每一张验证码图片拆成四张字符图片并保存
for filename in fileList:
    processed_img = ImageProcessing.img_processing(train_path + filename)
    for i in range(4):
        processed_img[i].save('./src/{}_{}.gif'.format(fileList.index(filename), i))
