#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/5 11:10
# @Author  : YoumingDong
# @File    : 20220205 get_def.py
# @Software: win10  python3.9

import rpa as r
import UrlModel as um
import OutputModel as op
# # 全局变量 用于记录递归次数
# global_recursion_counter = 1


def if_listed_company():
    '''
    判断是否是上市公司
    :return: 如果是返回True ,如果不是返回false
    '''
    text1 = um.get_text("body > div > div.company-detail > div:nth-child(4) > div > div > div.nav-head > a:nth-child(1) > h2")
    # shareholder_name.find('有限合伙') != -1
    if text1.find("上市信息") != -1 or text1.find("申报信息") != -1:
        return True
    else:
        return False



def executive_distinguish():
    # dom = 0  时，就是返回空
    # #mainmember > div:nth-child(3) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    r.dom("a229 = 0")
    # r.dom("if (document.querySelector('#partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a')){a229 = 1}")
    # 如果他存在有child3，说明其不仅有最新公示，还有工商登记，则label=1
    r.dom(
            "if (document.querySelector('#mainmember > div:nth-child(3) > div.app-ntable > table > "
            "tr:nth-child(2) > td.left > div > div > span.cont > span > a')){a229 = 1}")
    # r.dom("if ('#mainmember > div:nth-child(3) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a'){a229 = 1}")
    lable = r.dom("return a229")
    if lable != '1':
        css_selector = "#mainmember > div > div.app-ntable > table > tr> td.left > div > div > span.cont > span"
        return css_selector
    else:
        css_selector = "#mainmember > div:nth-child(2) > div.app-ntable > table > tr > td.left > div > div > span.cont > span > a"
        return css_selector

def get_executive():
    '''
    :return: [ ["顾敏","董事长,法定代表人"], ["李南青","总经理,董事"] ]
    '''
    # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    css_orign = executive_distinguish() # "#mainmember > div > div.app-ntable > table > tr> td.left > div > span.cont > span"
    num = um.get_num(css_orign)  # if num = 5 [ [],[],[],[],[],
    if num != '':
        num = int(num)
        result = []
        # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td:nth-child(5) > span
        if if_listed_company():
            for index in range(2, 2 + num):
                css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > div > span.cont > span"
                mainmember = r.read(css_temp1)
                if mainmember != '':
                    css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(3) > div > span"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
        else:
            for index in range(2, 2 + num):
                css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > div > span.cont > span"
                mainmember = r.read(css_temp1)
                if mainmember != '':
                    css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(3)  > div > span"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
    else:
        return []

#20200821 qyz:添加判断主要人员函数 使用xpath方法
def mainmember_distinguish_xpath():
    '''
    获取数量
    '''
    xpath_shareholder_1 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr/td[2]/div/span[2]/span[1]/a'''
    xpath_shareholder_2 = '''//*[@id="mainmember"]/div[3]/div[2]/table/tr/td[2]/div/span[2]/span[1]/a'''

    num1 = r.count(xpath_shareholder_1)
    num2 = r.count(xpath_shareholder_2)

    num_result = max(int(num1), int(num2))
    return num_result


#20220821qyz: 修改css为xpath
# #partner > div:nth-child(2) > div.tcaption > span.title-tab > span:nth-child(2) > a > span:nth-child(1)
def get_firstexecutive():
    '''
    :return: [ ["顾敏","董事长,法定代表人"], ["李南青","总经理,董事"] ]
    '''
    # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    num = mainmember_distinguish_xpath()
    if num != 0:
        result = []
        #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td:nth-child(5) > span
        if if_listed_company():
            for index in range(2, 2 + num):
                css_temp1 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr['''+str(index)+''']/td[2]/div/span[2]/span[1]/a'''
                #css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > div > span.cont > span"
                mainmember = r.read(css_temp1)
                if mainmember != '':
                    css_temp2 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr['''+str(index)+''']/td[5]'''
                    #css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(3) > div > span"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
        else:
            for index in range(2, 2 + num):
                css_temp1 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr['''+str(index)+''']/td[2]/div/span[2]/span[1]/a'''
                #css_temp1 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td.left > div > div > span.cont > span"
                mainmember = r.read(css_temp1)
                if mainmember != '':
                    css_temp2 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr['''+str(index)+''']/td[3]'''
                    #css_temp2 = "#mainmember > div > div.app-ntable > table > tr:nth-child(" + str(index) + ") > td:nth-child(3)  > div > span"
                    mainmember_job = r.read(css_temp2)
                    result.append([mainmember, mainmember_job])
                else:
                    pass
            return result
    else:
        return []
    # #mainmember > div > div.app-ntable > table > tr:nth-child(2) > td:nth-child(3) > div > span
    # 主要人员姓名
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span
    # mainmember > div > div.app-ntable > table > tr:nth-child(3) > td.left > div > span.cont > span
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span
    # #mainmember > div > div.app-ntable > table > tr> td.left > div > span.cont > span
    # 主要人员职务
    # mainmember > div > div.app-ntable > table > tr:nth-child(2) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(3) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(4) > td:nth-child(3)
    # mainmember > div > div.app-ntable > table > tr:nth-child(5) > td:nth-child(3)
    # #mainmember > div > div.app-ntable > table > tr > td:nth-child(3)

def get_shareholding_ratio():
    '''

    :return: ["40%","50%",]
    '''
    # partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td:nth-child(3)
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td:nth-child(3)
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(3) > td:nth-child(3)
    css_selector = shareholder_distinguish()
    num = int(um.get_num(css_selector))
    result = []
    for index in range(2, 2 + num):
        # css_temp = "#partner > div.tablist > div.app-tree-table > table > tr:nth-child(" + str(index) + ") > td:nth-child(3)"
        # shareholding_ratio = r.read(css_temp)
        # if shareholding_ratio != '':
        #     shareholding_ratio = shareholding_ratio.split("%",1)[0]
        #     result.append(shareholding_ratio)
        # else:
        #     pass
        result.append("-")
    return result


# 正常的
# #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
# #partner > div:nth-child(3) > div.sub-section > div > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a

# 最新公示
# #partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a
# 工商登记
# #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a

# #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a


# #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
# #partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
# #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a 工商登记
def shareholder_distinguish():
    # dom = 0  时，就是返回空
    r.dom("a229 = 0")
    # r.dom("if (document.querySelector('#partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a')){a229 = 1}")
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    r.dom("if (document.querySelector('#partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a')){a229 = 1}")
    lable = r.dom("return a229")
    if lable != '1':
        css_selector = "#partner > div > div.app-tree-table > table > tr > td.left > div > span.cont > span > a"
        return css_selector
    else:
        css_selector = "#partner > div:nth-child(2) > div.app-tree-table > table > tr > td.left > div > span.cont > span > a"
        return css_selector
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    # #partner > div > div.app-tree-table > table > tr:nth-child(2) > td.left > div > span.cont > span > a

def get_shareholder_num():
    css_selector = shareholder_distinguish()
    a = um.get_num(css_selector)
    num = int(a)
    return num

def if_can_get(company_name):
    css_selector = shareholder_distinguish()
    num_flag = 0
    for i in range(3):
        try:
            a = um.get_num(css_selector)
            num = int(a)
        except ValueError:
            # 如果加载全了，还不能获取，就返回False
            if um.if_complete() and (not op.recursion_counter_if3()):
                print("!!!!!")
                print(company_name + "疑似出现问题,但已经跳过。")
                print("!!!!!")
                return company_name
            print("shareholder获取失败，正在重新尝试")
            if i < 2:
                r.wait(5)
        else:
            num_flag = 1
            break
    if num_flag == 0:
        print("shareholder获取失败，已退回" + company_name + "疑似出现问题。")
        int("")
    # 正常情况下，return True
    return True

def get_shareholder():
    '''
    return [ [zxy,a],[dym,a]]
    '''
    num = get_shareholder_num()
    result = []
    for index in range(2, 2 + num):
        css_temp = "#partner > div.tablist > div.app-tree-table > table.ntable > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span > a"
        shareholder = r.read(css_temp)
        if shareholder != '':
            get_url = get_url_cssSelector("#partner > div.tablist > div.app-tree-table > table.ntable > tr:nth-child(" + str(index) + ") > td.left > div > span.cont > span > a")
            result.append([shareholder, get_url])
        else:
            pass
    return result



def get_url_cssSelector(css):
    # tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a
    js1 = '''element = document.querySelector(' ''' + css +''' ')'''
    js2 = '''return element.href'''
    r.dom(js1)
    url = r.dom(js2)
    return url

def get_url_xpath(xpath):
    result = r.read(xpath+"/@href")
    return result

if __name__ == '__main__':
    r.tagui_location(r"D:")
    r.init()
    #url_init = r'https://www.qcc.com/firm/5b75938e604b0bf4b69fddb016339b70.html'  #深圳市信丰网物流有限公司
    url_init = r'https://www.qcc.com/firm/81d02fee056d6bb632440d29114f616f.html'  #佛山信仁货运代理有限公司
    #url_init = r'https://www.qcc.com/firm/bf69a9651df2bae5ffbf2219848387bf.html' #深圳市丰捷信物流有限公司

    # 实例化谷歌设置选项

    r.url(url_init)  # 打开网页了
    r.wait(8)  # 等待

    print(get_executive())
    print(get_shareholding_ratio())
    print(get_shareholder())


    # #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a
    # #partner > div:nth-child(2) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.ipo-partner-app-tdcoy > span.cont > span > a
    # #partner > div:nth-child(3) > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a

    # #partner > div.tablist > div.app-tree-table > table > tr:nth-child(2) > td.left.first-td > div.td-coy.partner-app-tdcoy > span.cont > span > a