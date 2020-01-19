# -*- encoding：utf-8 -*-
"""
@project: Cracking_Verification_Code
@author: why
@file: getInfo.py
@ide: PyCharm
@time: 2020/1/1718:22
"""
import requests
import urllib
import Login
from bs4 import BeautifulSoup, element
from Login import login
from config import get_data

# 获取信息链接后缀
getInfoSuffix = '/xs_main.aspx?xh=' + get_data('stu1', 'xh')
getScoreInfoSuffix = '/mycjcx/xscjcx.asp?'
getClassTableInfoSuffix = '/xskbcx.aspx?'
getExamTimeInfoSuffix = 'xskscx.aspx?'
# 获取信息响应头
getInfoHeaders = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cache-Control': "max-age=0",
    'Cookie': "ASP.NET_SessionId=wfmtslfxm4mmjcnzabnqn455; SF_cookie_1=98184645",
    'Host': "202.206.243.62",
    'Referer': "http://202.206.243.62/default2.aspx",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}
# 获取信息传入数据
getInfoData = {
    'xh': get_data('stu1', 'xh'),
}
# 获取详细信息响应头
getDetailedInfoHeaders = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "ASP.NET_SessionId=wfmtslfxm4mmjcnzabnqn455; SF_cookie_1=98184645",
    'Host': "202.206.243.62",
    'Proxy-Connection': "keep-alive",
    'Referer': "http://202.206.243.62/xs_main.aspx?xh=" + get_data('stu1', 'xh'),
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}
# 获取详细信息传入数据
getDetailedInfoData = {
    'xh': get_data('stu1', 'xh'),
    'xm': "",
    'gnmkdm': "",
}
# 学年学期信息传入数据
getTermInfoData = {
    # todo 通过某种方式提前获取到VIEWSTATE，从而实现不同学期信息的查询
    # 只能查询到当前学期的数据。。。（可能
    # '__EVENTTARGET': "xnd",
    # '__EVENTARGUMENT': "",
    # # __VIEWSTATE会根据学期、学年、查询项目、姓名等的不同而变化，但是变化是固定的，加密方式为BASE64，或许可以先GET？
    # '__VIEWSTATE': "",
    'xnd': "2019-2020",
    'xqd': "1"
}


def get_info(info_index):
    login()
    html = requests.get(Login.urlPrefix + getInfoSuffix, headers=getInfoHeaders, data=getInfoData).text
    bs = BeautifulSoup(html, "html.parser")
    result = bs.find('span', id='xhxm').get_text()
    xm = result.split('同学')[0]
    getDetailedInfoData['xm'] = xm
    # 查询成绩功能
    if info_index == 1:
        course_list = []

        # 设置科目类
        class Course(object):
            def __init__(self):
                self.school_year = ''
                self.school_term = 0
                self.course_id = ''
                self.course_name = ''
                self.teacher_id = ''
                self.course_type = ''
                self.course_assignment = ''
                self.credit = 0.0
                self.achievement_point = 0.0
                self.achievement = ''
                self.make_up_exam_achievement = ''
                self.remark = ''
                self.rebuild_flag = False
                self.minor_flag = False
                self.degree_course_flag = ''

            def save_info(self, info_list):
                self.school_year = info_list[1].split('\\')[0]
                self.school_term = int(info_list[2].split('\\')[0])
                self.course_id = info_list[3].split('\\')[0]
                self.course_name = info_list[4].split('\\')[0]
                self.teacher_id = info_list[5].split('\\')[0]
                self.course_type = info_list[6].split('\\')[0]
                self.course_assignment = info_list[7].split('\\')[0]
                self.credit = float(info_list[8].split('\\')[0])
                self.achievement_point = float(info_list[9].split('\\')[0])
                self.achievement = info_list[10].split('\\')[0]
                self.make_up_exam_achievement = info_list[11].split('\\')[0]
                self.remark = info_list[12].split('\\')[0]
                self.rebuild_flag = bool(info_list[13].split('\\')[0])
                self.minor_flag = bool(info_list[14].split('\\')[0])
                self.degree_course_flag = True if (info_list[15].split(' ')[0] == '是') else False
                return self

        # 设置查询成绩功能模块代码
        getDetailedInfoData['gnmkdm'] = "N121632"
        url = Login.urlPrefix + getScoreInfoSuffix + urllib.parse.urlencode(getDetailedInfoData, encoding='gb2312')
        info = requests.get(url, headers=getDetailedInfoHeaders, data=getDetailedInfoData)
        info.encoding = 'gb2312'
        bs = BeautifulSoup(info.text, "html.parser")
        blocks = bs.findAll('tr', bgcolor="#D0E8FF")
        for block in blocks:
            info_str = block.get_text()
            info_list = info_str.split('\n')
            if len(info_list) > 15:
                course = Course().save_info(info_list)
                course_list.append(course)
        print(course_list)
    # 查询个人课表功能
    elif info_index == 2:
        school_table = []

        # 定义课程类
        class ClassInfo(object):
            def __init__(self):
                self.have_class = False
                self.class_name1 = ''
                self.class_type1 = ''
                self.class_time1 = ''
                self.class_teacher1 = ''
                self.classroom1 = ''
                self.have_class2 = False
                self.class_name2 = ''
                self.class_type2 = ''
                self.class_time2 = ''
                self.class_teacher2 = ''
                self.classroom2 = ''

            def save_info(self, info_list):
                self.have_class = True
                self.class_name1 = info_list[0]
                self.class_type1 = info_list[2]
                self.class_time1 = info_list[4]
                self.class_teacher1 = info_list[6]
                self.classroom1 = info_list[8]
                for index in range(8, len(info_list), 2):
                    if type(info_list[index]) == element.Tag:
                        self.have_class2 = True
                        self.class_name2 = info_list[index + 1]
                        self.class_type2 = info_list[index + 3]
                        self.class_time2 = info_list[index + 5]
                        self.class_teacher2 = info_list[index + 7]
                        self.classroom2 = info_list[index + 9]
                        break
                return self

        # 设置查询个人课表功能模块代码
        getDetailedInfoData['gnmkdm'] = "N121603"
        url = Login.urlPrefix + getClassTableInfoSuffix + urllib.parse.urlencode(getDetailedInfoData, encoding='gb2312')
        getDetailedInfoHeaders['Referer'] = url
        info = requests.post(url, headers=getDetailedInfoHeaders, data={**getDetailedInfoData, **getTermInfoData})
        # info = requests.get(url, headers=getDetailedInfoHeaders)
        info.encoding = 'gb2312'
        # print(info.text)
        bs = BeautifulSoup(info.text, "html.parser")
        # print(info.text)
        # getTermInfoData['__EVENTTARGET'] = bs.find('input', name="__EVENTTARGET").get('value')
        # getTermInfoData['__EVENTARGUMENT'] = bs.find('input', name="__EVENTARGUMENT").get('value')
        # getTermInfoData['__VIEWSTATE'] = bs.find('input', name="__VIEWSTATE").get('value')
        class_table = bs.find_all('table', attrs={"class": "blacktab"})
        index = 0
        class_info = class_table[0].tr
        for i in range(14):
            if index % 2 == 0 and index != 0:
                temp_class_info = class_info.find_all('td', align="Center")
                school_table_week = []
                for each_class_info in temp_class_info:
                    if each_class_info.get('rowspan') == "2":
                        temp_class = ClassInfo().save_info(each_class_info.contents)
                        school_table_week.append(temp_class)
                    else:
                        temp_class = ClassInfo()
                        school_table_week.append(temp_class)
                school_table.append(school_table_week)
            index = index + 1
            class_info = class_info.next_sibling
        print(school_table)
    # 查询考试时间功能
    elif info_index == 3:
        # 设置查询考试功能模块代码
        getDetailedInfoData['gnmkdm'] = "N121604"
        url = Login.urlPrefix + getExamTimeInfoSuffix + urllib.parse.urlencode(getDetailedInfoData, encoding='gb2312')
        getDetailedInfoHeaders['Referer'] = url
        info = requests.post(url, headers=getDetailedInfoHeaders, data={**getDetailedInfoData, **getTermInfoData})
        info.encoding = 'gb2312'
        print(info.text)
        # todo 查询考试时间的数据处理
    elif info_index == 4:
        # todo 查询实验课程的处理
        pass


if __name__ == '__main__':
    get_info(2)
