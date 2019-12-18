# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: Login.py
@ide: PyCharm
@time: 2019/12/17 21:19
"""
import requests
from io import BytesIO
from PIL import Image

urlPrefix = 'http://202.206.243.62/'
loginSuffix = '/default2.aspx'
getCheckCodeSuffix = '/CheckCode.aspx'
getInfoSuffix = '/xs_main.aspx?xh=170104010053'
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
loginData = {
    '__VIEWSTATE': "dDwxNTMxMDk5Mzc0Ozs+cgOhsy/GUNsWPAGh+Vu0SCcW5Hw=",
    'txtUserName': "170104010053",
    'Textbox1': "",
    'TextBox2': "",
    'txtSecretCode': "",
    'RadioButtonList1': "%D1%A7%C9%FA",
    'Button1': "",
    'lbLanguage': "",
    'hidPdrs': "",
    'hidsc': "",
}
getInfoHeaders = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "max-age=0",
    'Cookie': "ASP.NET_SessionId=wfmtslfxm4mmjcnzabnqn455; SF_cookie_1=98184645",
    'Host': "202.206.243.62",
    'Referer': "http://202.206.243.62/default2.aspx",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
}
getInfoData = {
    'xh': "170104010053"
}


# 得到验证码图片
def get_check_code():
    resp = requests.get(urlPrefix + getCheckCodeSuffix, headers=loginHeaders)
    # print(resp.content)
    # bytes转字节流
    bytes_stream = BytesIO(resp.content)
    img = Image.open(bytes_stream)
    # img.show()
    return img


# 登录教务系统
def login():
    loginResp = requests.post(urlPrefix + loginSuffix, headers=loginHeaders, data=loginData)
    # print(loginResp.text)
    getInfoResp = requests.get(urlPrefix + getInfoSuffix, headers=getInfoHeaders, data=getInfoData)
    print(getInfoResp.text)


if __name__ == '__main__':
    get_check_code().show()
    checkCode = input("输入验证码：")
    loginData['txtSecretCode'] = checkCode
    login()
