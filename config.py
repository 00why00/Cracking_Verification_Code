# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: config.py
@ide: PyCharm
@time: 2020/1/1714:31
"""
# 读取学号和密码等敏感信息
import configparser
import os


def get_data(section, data_name):
    """
    得到data.ini文件中的敏感信息
    :param section: 信息所在的标签
    :param data_name: 要得到的信息的key
    :return: 要得到的信息的value
    """
    # 用os模块来读取
    cur_path = os.path.dirname(os.path.realpath(__file__))
    cfg_path = os.path.join(cur_path, "src/data.ini")

    # 调用读取配置模块中的类
    conf = configparser.ConfigParser()
    conf.read(cfg_path)

    # 调用get方法，然后获取配置的数据
    return conf.get(section, data_name)
