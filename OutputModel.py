#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 13:08
# @Author  : YoumingDong
# @File    : OutputModel.py
# @Software: win10  python3.9
import numpy as np
import pandas
import pandas as pd
import xlwt
# 全局变量 用于记录递归次数
global_recursion_counter = 0

# 全局变量 用于记录写入行数
global_company_name = ""
global_index_num = np.NAN
global_sub_bank = np.NAN
global_table_list = []

def recursion_counter_up():
    global global_recursion_counter
    global_recursion_counter += 1

def recursion_counter_down():
    global global_recursion_counter
    global_recursion_counter = global_recursion_counter - 1

def recursion_counter_init():
    global global_recursion_counter
    global_recursion_counter = 0

def recursion_counter_checkfirst():
    global global_recursion_counter
    if global_recursion_counter == 1:
        return True
    else:
        return False

def recursion_counter_if1():
    '''
    判断是否进行了穿刺
    :return:进行了返回ture,没进行返回false
    '''
    global global_recursion_counter
    if global_recursion_counter >= 2:
        return True
    else:
        return False

def recursion_counter_if2():
    '''
    判断是否继续进行穿刺
    :return:
    '''
    global global_recursion_counter
    if global_recursion_counter >= 3:
        return False
    else:
        return True


def company_getter(company_name, index_num, sub_bank):
    global global_recursion_counter
    global global_company_name
    global global_index_num
    global global_sub_bank
    if global_recursion_counter == 1:
        global_company_name = company_name
        global_index_num = index_num
        global_sub_bank = sub_bank
    else:
        pass

# def root_company_name():
#     global global_recursion_counter
#     global global_company_name
#     if global_recursion_counter == 1:
#         global_company_name = company_name
#     else:
#         pass
#     pass

def result_output1(shareholder_list1, key_person_list3, company_name):
    table1 = pd.read_excel(r"data\output.xlsx")
    name_list = [x[0] for x in shareholder_list1] + [x[0] for x in key_person_list3]
    row_num = len(shareholder_list1) + len(key_person_list3)
    career = [x[1] for x in key_person_list3]
    # 如果模板加字段，这里要更改
    table2 = pd.DataFrame(np.full((row_num, len(table1.columns)), "-"), columns=table1.columns)
    table2["姓名"] = name_list
    for index in range(0, row_num):
        if index < len(shareholder_list1):
            table2.loc[index,"是否股东"] = "是"
            # table2.loc[index,"持股比例"] = ratio_list2[index]
        else:
            table2.loc[index,"是否主要人员"] = "是"
            table2.loc[index,"职务"] = career[index - len(shareholder_list1)]
    global global_company_name
    global global_index_num
    global global_sub_bank
    if recursion_counter_if1():
        table2["公司"] = global_company_name
        table2["是否为合伙企业中的股东"] = company_name
        table2["序号"] = global_index_num
        table2["管辖支行"] = global_sub_bank
    else:
        table2["公司"] = company_name
        # global global_index_num
        table2["序号"] = global_index_num
        # global global_sub_bank
        table2["管辖支行"] = global_sub_bank
    result_table = pd.concat([table1,table2])
    result_table.to_excel("data\output.xlsx", index=None)
    pass

def recursion_counter_if3():
    '''
    如果是母公司，return True，不是就return False
    :return:
    '''
    global global_recursion_counter
    if global_recursion_counter == 0:
        return True
    else:
        return False

def init_output():
    global global_table_list
    columns = ["序号", "公司", "姓名", "是否股东", "持股比例", "是否主要人员", "职务", "是否为合伙企业中的股东", "支行名称"]
    table2 = pd.DataFrame( columns=columns)
    global_table_list = [table2]


def get_table(table):
    global global_table_list
    global_table_list.append(table)

def table_output():
    global global_table_list
    global global_index_num
    global global_company_name
    result_table = pd.concat(global_table_list)
    file_name = "result\\" + global_index_num + "_" + global_company_name + "output.xlsx"
    result_table.to_excel(file_name, index=None)


def result_output(shareholder_list1, key_person_list3, company_name):
    columns = ["序号","公司",	"姓名","是否股东","持股比例","是否主要人员","职务","是否为合伙企业中的股东","支行名称"]
    name_list = [x[0] for x in shareholder_list1] + [x[0] for x in key_person_list3]
    row_num = len(shareholder_list1) + len(key_person_list3)
    career = [x[1] for x in key_person_list3]
    # 如果模板加字段，这里要更改
    table2 = pd.DataFrame(np.full((row_num, len(columns)), "-"), columns=columns)
    table2["姓名"] = name_list
    for index in range(0, row_num):
        if index < len(shareholder_list1):
            table2.loc[index, "是否股东"] = "是"
            # table2.loc[index,"持股比例"] = ratio_list2[index]
        else:
            table2.loc[index, "是否主要人员"] = "是"
            table2.loc[index, "职务"] = career[index - len(shareholder_list1)]
    global global_company_name
    global global_index_num
    global global_sub_bank
    if recursion_counter_if1():
        table2["公司"] = global_company_name
        table2["是否为合伙企业中的股东"] = company_name
        table2["序号"] = global_index_num
        table2["管辖支行"] = global_sub_bank
    else:
        table2["公司"] = company_name
        # global global_index_num
        table2["序号"] = global_index_num
        # global global_sub_bank
        table2["管辖支行"] = global_sub_bank
    get_table(table2)
    pass

if __name__ == '__main__':
    shareholder_list1 = [["a1","b1"],["a2","b2"],["a3","b3"]]
    key_person_list3 = [["c1", "d1"], ["d2", "d2"], ["d3", "d3"],["d4", "d4"]]
    ratio_list2 = ["g1", "g2", "g3"]
    company_name = "test"
    result_output(shareholder_list1,ratio_list2,key_person_list3,company_name)