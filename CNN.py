# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: CNN.py
@ide: PyCharm
@time: 2020/1/1516:28
"""
# 构建卷积神经网络识别验证码
import os
import string
import glob
import numpy as np
from PIL import Image
import keras
from keras import layers, activations, models, optimizers, losses

num_classes = 36
batch_size = 128
epochs = 40

# 输入图片尺寸
img_rows, img_cols = 12, 22

character = string.ascii_lowercase + string.digits
os.chdir(r'./train_pictures')

if keras.backend.image_data_format == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)

X, Y = [], []

for f in glob.glob('*.png')[:]:
    image = Image.open(f)
    im = image.point(lambda i: i != 43, mode='1')

    y_min, y_max = 0, 22
    split_lines = [5, 17, 29, 41, 53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]

    name = f.split('.')[0]
    for i, im in enumerate(ims):
        t = 1.0 * np.array(im)
        t = t.reshape(*input_shape)
        X.append(t)  # 验证码像素列表

        s = name[i]
        Y.append(character.index(s))  # 验证码字符

X = np.array(X)
Y = np.array(Y)
Y = keras.utils.to_categorical(Y, num_classes)
split_point = 3000
x_train, y_train, x_test, y_test = X[:split_point], Y[:split_point], X[split_point:], Y[split_point:]

model = models.Sequential([
    # 输入的shape为[22, 12, 1]
    layers.Conv2D(filters=32, kernel_size=(3, 3), activation=activations.relu, input_shape=input_shape),
    # 卷积后shape为[22, 12, 32]
    layers.Conv2D(filters=64, kernel_size=(3, 3), activation=activations.relu),
    # 卷积后shape为[22, 12, 64]
    layers.MaxPool2D(pool_size=(2, 2)),
    # 池化后shape为[11, 6, 64]
    layers.Flatten(),
    # 平坦化shape为[1, 1, 4556]
    layers.Dense(units=512, activation=activations.relu),
    # 全连接shape为[1, 1, 512]
    layers.Dropout(rate=0.5),
    # 丢弃率为45%
    layers.Dense(units=num_classes, activation=activations.softmax)
    # 全连接shape为[1, 1, 36]
])

model.compile(optimizer=optimizers.Adadelta(),
              loss=losses.categorical_crossentropy,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

os.chdir('..')
model.save('cnn.h5')
