# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: get_checkCode.py
@ide: PyCharm
@time: 2019/12/17 21:19
"""
import requests
from io import BytesIO
from PIL import Image

urlPrefix = 'http://202.206.243.62/'
loginSuffix = '/default2.aspx'
getCheckCodeSUffix = '/CheckCode.aspx'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    'Cookie': "ASP.NET_SessionId=wtw154eyqwn3ozy03wp00eaj; SF_cookie_1=98184645",
    'Host': "202.206.243.62"
}

# 得到验证码图片
resp = requests.get(urlPrefix + getCheckCodeSUffix)
# print(resp.content)
# bytes转字节流
bytes_stream = BytesIO(resp.content)
img = Image.open(bytes_stream)
# img.show()


