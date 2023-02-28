#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/3 12:05
# @Author  : YoumingDong
# @File    : 20220203rpa_test.py
# @Software: win10  python3.9

import rpa as r
import pandas as pd
import UrlModel as um
import getModel as gm
import OutputModel as op
import os



global_company_error_list = []

def edge_on():
    '''
    浏览器启动
    :return:
    '''
    r.tagui_location(r"D:\pycharm")
    r.init()




def search_name(company_name):
    '''
    从主页开始查 某个company_name
    :param diver:
    :param company_name:
    :return:
    '''

    url_init = r'https://www.qcc.com/'  # 网址

    # 实例化谷歌设置选项

    um.go_href(url_init)
    r.wait(1)
    r.type("#searchKey", company_name)
    r.wait(2)
    um.my_click('body > div > div.app-home > section.nindex-search > div > div > div > div.app-search-input.big > div > div > span > button')
    #old
    #url2 = um.get_url_cssSelector("tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a")
    #update20221127
    url2 = um.get_url_cssSelector('body > div > div.app-search > div.container.m-t > div.adsearch-list > div > div.msearch.select-search-enable > div > table > tr.frtrt.tsd0 > td:nth-child(3) > div > span > span.copy-title > a')
    # um.my_click("tr:nth-child(1) > td:nth-child(3) > div > div.app-copy-box.copy-hover-item > span.copy-title > a")
    #old
    #print(url2)
    um.go_href(url2)
    #um.my_click('body > div > div.app - search > div.container.m - t > div.adsearch - list > div > div.msearch.select - search - enable > div > table > tr.frtrt.tsd0 > td: nth - child(3) > div > span > span.copy - title > a')
    if gm.if_listed_company():
        # um.my_click(
        #     'body > div > div.app-search > div.container.m-t > div.adsearch-list > div > div.msearch.select-search-enable > div > table > tr.frtrt.tsd0 > td:nth-child(3) > div > span > span.copy-title > a > span')
        r.click("body > div > div.company-detail > div:nth-child(4) > div > div > div.nav-head > a:nth-child(2) > h2")
    pass

def shareholder_output(shareholder_list1,ratio_list2):
    for a,b in zip(shareholder_list1,ratio_list2):
        print(a[0] + ":" + b + "\n")

def key_person_output(key_person_list3):
    for key_person in key_person_list3:
        print(key_person[0] + ":" + key_person[1] + "\n")


def shareholder_main(company_name, index_num, sub_bank):
    print("START-" + company_name + "-START")
    op.recursion_counter_up()
    op.company_getter(company_name, index_num, sub_bank)

    shareholder_list1 = gm.get_shareholder()
    # ratio_list2 = gm.get_shareholding_ratio()
    if op.recursion_counter_checkfirst():
        key_person_list3 = gm.get_firstexecutive()
    else:
        key_person_list3 = gm.get_executive()


    # shareholder_output(shareholder_list1, ratio_list2, key_person_list3)
    # key_person_output(key_person_list3)
    op.result_output(shareholder_list1, key_person_list3,company_name)

    for element in shareholder_list1:
        shareholder_name = element[0]
        href = element[1]
        # print(executive)
        #if (shareholder_name.find('有限合伙') != -1) and (op.recursion_counter_if2()):
        if (shareholder_name.find('有限合伙') != -1) and (op.recursion_counter_if2()) and (shareholder_name.find('投资') == -1) and (shareholder_name.find('天使') == -1 ) and (shareholder_name.find('基金') == -1):# todo：增加天使、基金、投资的优化
            # search_name(driver, shareholder_name)
            um.go_href(href)
            probe = gm.if_can_get(shareholder_name)
            if probe is True:
                shareholder_main(shareholder_name, index_num, sub_bank)
            else:
                global global_company_error_list
                global_company_error_list.append(probe)
                pass
        else:
            # print(1)
            pass
    print("FINISH-" + company_name + "-FINISH")
    op.recursion_counter_down()
    um.go_back()
    pass


def company_selector(index1, index2):
    index1 -= 1
    index2 -= 1
    sub_company = cn_table[index1:index2]
    company_name = sub_company["公司"]
    index_num = sub_company["序号"]
    sub_bank = sub_company["管辖支行"]
    return company_name, index_num, sub_bank

def company_selector2(index1):
    index1 = [x-1 for x in index1]
    sub_company = cn_table.iloc[index1,:]
    company_name = sub_company["公司"]
    index_num = sub_company["序号"]
    sub_bank = sub_company["管辖支行"]
    return company_name, index_num, sub_bank

if __name__ == '__main__':
    # time_delay()
    # print(1)

    # global global_company_error_list
    ##################################
    excel_path = r"data/公司.xlsx"
    cn_table = pd.read_excel(excel_path, dtype='string')

    # 输入序号
    #company_name_list, index_list, sub_bank_list = company_selector(212, 254+1)   # 453,454
    # error_list2 = ['64']
    '''跑错误的用下面代码'''
    error_list2 =  ['109', '189', '195', '197', '217', '218', '219', '220', '224', '231', '232', '233', '234', '235', '236', '239', '243', '244', '245', '246', '247', '248', '250', '251']
    b = list(map(int, error_list2))
    company_name_list, index_list, sub_bank_list = company_selector2(b)

    # company_name_list = ["深圳市安聚源投资企业（有限合伙）"]
    # index_list = [""]
    # sub_bank_list = ["test"]
    edge_on()
    error_list = []
    for company_name, index, sub_bank in zip(company_name_list, index_list,sub_bank_list):
        op.recursion_counter_init()

        try:
            print("序号：" + index + " 开始获取")
            search_name(company_name)
            op.init_output()
            shareholder_main(company_name, index, sub_bank)
            op.table_output()
        except ValueError:
            print(index + ":error,请重试")
            error_list.append(index)
            op.table_output()
            os.system("a.wav")
            r.wait(10)
            r.close()
            r.wait(5)
            edge_on()
            r.wait(5)


        # else:
        #     op.table_output()
        #     print("序号：" + index + " 获取完成！")
        print("当前错误序号：")
        print(error_list)
        print(global_company_error_list)





# ['644', '762', '774','805']
# ['554', '595', '612', '616', '617', '618', '619', '620', '621', '622', '623', '624', '626', '627', '628', '629', '630', '631', '632', '633', '634', '635', '636', '637', '638', '644', '646', '647', '649', '650', '651', '652', '653', '657', '658', '664', '665', '668', '670', '671', '672', '673', '674', '675', '676', '677', '678', '679', '680', '681', '682', '683', '684', '685', '686', '687', '688', '690', '691', '692', '694', '696', '697', '705', '708', '717', '720', '721', '722', '723', '724', '725', '727', '741', '742', '743', '744', '751', '754', '756', '758', '760', '762', '767', '774', '776', '781', '783', '789', '790', '792', '793', '794', '795', '796', '798']
    pass

