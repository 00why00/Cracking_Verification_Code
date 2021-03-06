# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: Login.py
@ide: PyCharm
@time: 2019/12/17 21:19
"""
# 登录教务系统
import requests
from config import get_data
from io import BytesIO
from PIL import Image
from predict import predict

# 教务系统链接前缀
urlPrefix = 'http://202.206.243.62/'
# 登录链接后缀
loginSuffix = '/default2.aspx'
# 获取验证码链接后缀
getCheckCodeSuffix = '/CheckCode.aspx'

# 登录响应头
loginHeaders = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "max-age=0",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cookie': "ASP.NET_SessionId=wfmtslfxm4mmjcnzabnqn455; SF_cookie_1=98184645",
    'Host': "202.206.243.62",
    'Referer': "http://202.206.243.62/default2.aspx",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
}
# 登录传入数据
loginData = {
    # 此处__VIEWSTATE的值不会改变
    '__VIEWSTATE': "dDwxNTMxMDk5Mzc0Ozs+cgOhsy/GUNsWPAGh+Vu0SCcW5Hw=",
    'txtUserName': get_data('stu1', 'xh'),
    'Textbox1': "",
    'TextBox2': get_data('stu1', 'psw'),
    'txtSecretCode': "",
    'RadioButtonList1': "%D1%A7%C9%FA",
    'Button1': "",
    'lbLanguage': "",
    'hidPdrs': "",
    'hidsc': "",
}


def get_check_code():
    """
    请求网址得到验证码图片
    :return: 验证码图片
    """
    resp = requests.get(urlPrefix + getCheckCodeSuffix, headers=loginHeaders)
    # print(resp.content)
    # bytes转字节流
    bytes_stream = BytesIO(resp.content)
    img = Image.open(bytes_stream)
    # img.show()
    return img


def login():
    """
    登录教务系统获取信息
    :return: 输出对应信息网页(后期改为获取信息)
    """
    check_code_img = get_check_code()
    # check_code_img.show()
    check_code = predict(check_code_img)
    # print(checkCode)
    loginData['txtSecretCode'] = check_code
    requests.post(urlPrefix + loginSuffix, headers=loginHeaders, data=loginData)


if __name__ == '__main__':
    login()
