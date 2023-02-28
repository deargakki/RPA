#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 19:57
# @Author  : YoumingDong
# @File    : 20220211data_analysis.py
# @Software: win10  python3.9

# 名字大于4的删除
# 同公司内去重

import numpy as np

import pandas as pd
import copy as copy
if __name__ == '__main__':
    excel_path = r"D:\RPA_project\rpa_demand1\result\outputFin.xlsx"
    cn_table = pd.read_excel(excel_path, dtype='string')
    cn_table = cn_table[~cn_table['姓名'].str.contains("公司|合作社|商行|有限合伙|Limited|Fund|企业|投资|中华人民共和国|理事会|基金会")]

    # index_list = [x for x in range(1627)]
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    index_list = [x for x in range(1,100)]
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    result_list = []
    for index in index_list:
        temp_table = cn_table[cn_table["序号"] == str(index)]
        temp_table1 = temp_table.drop_duplicates(['公司','姓名','是否股东','持股比例','是否主要人员','职务'])
        temp_table2 = copy.deepcopy(temp_table1)
        # temp_result= pd.merge(temp_table1,temp_table2,on=[])
        temp_table1 = temp_table1[['序号','公司', '姓名', '是否股东', '是否为合伙企业中的股东', '管辖支行']]
        temp_table1 = temp_table1[~temp_table1['是否股东'].str.contains("-")]

        temp_table2 = temp_table2[['序号','公司', '姓名', '是否主要人员', '职务','是否为合伙企业中的股东', '管辖支行']]
        temp_table2 = temp_table2[~temp_table2['是否主要人员'].str.contains("-")]
        temp_result = pd.merge(temp_table1, temp_table2, on=['公司', '姓名','序号','管辖支行'], how='outer')
        result_list.append(temp_result)
        pass
        print(index)

    result = pd.concat(result_list)
    result.to_excel(r"D:\RPA_project\rpa_demand1\result\20220213output2.0.xlsx", index=False)
    #temp_table = temp_table['公司','姓名'	,'是否股东','持股比例','是否主要人员','职务','是否为合伙企业中的股东','支行名称','管辖支行']