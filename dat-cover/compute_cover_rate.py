"""
function：计算网点覆盖率
author： ssy
"""

import pandas as pd
import numpy as np

global branch_bank_list
global cn_report
global cn_company


def compute_require_company(df):
    """
    计算要求公司数
    :param :
    :return: 统计结果
    """

    # 统计要求公司数
    df_num = df.groupby("管辖行").count()
    df_num = df_num.drop(["公司中文名称"], axis=1)
    df_num = df_num.drop(["网点"], axis=1)
    df_num = df_num.rename(columns={"序号": "计数项:公司个数"})

    # 双重遍历计数
    # global branch_bank_list
    # branch_bank_list = cn_company["管辖"].drop_duplicates()
    # required_company_num = np.zeros((len(branch_bank_list), 1))
    # df_num = pd.DataFrame(required_company_num, columns=["计数项:公司个数"], index=branch_bank_list)
    #
    # for index, row in cn_company.iterrows():
    #     for bank in branch_bank_list:
    #         if row["管辖"] == bank:
    #             df_num.loc[bank]["计数项:公司个数"] = df_num.loc[bank]["计数项:公司个数"] + 1

    return df_num


def compute_completed_company(df):
    """
    计算true公司数
    :param df: 公司表
    :return: 统计结果
    """
    # col_name = df.columns.tolist()

    # if '计数项:公司个数' in col_name:
    #     df_num = df.groupby('管辖行（建议）')['计数项:公司个数'].sum()
    # else:
    #
    df_num = df.groupby('管辖行（建议）')['公司'].count()
    # df_num = df_num.drop(["序号"], axis=1)
    # df_num = df_num.rename({"计数项:公司个数": "公司"})

    # global branch_bank_list
    #
    # completed_company_num = np.zeros((len(branch_bank_list), 1))
    # df_num = pd.DataFrame(completed_company_num, columns=["计数项:公司个数"], index=branch_bank_list)
    #
    # for index, row in df.iterrows():
    #     for bank in branch_bank_list:
    #         if row["管辖行（建议）"] == bank:
    #             df_num.loc[bank]["计数项:公司个数"] = df_num.loc[bank]["计数项:公司个数"] + 1
    return df_num


def new_column_maker(path):
    """
    处理多级表头
    :param path: 原数据excel路径
    :return: 单级表头dataframe
    """

    df_1 = pd.read_excel(open(path, 'rb'), sheet_name="报备客户底表", header=[0, 1])
    df_2 = pd.read_excel(open(path, 'rb'), sheet_name="报备客户底表", header=1)

    index_a = df_1.columns.get_level_values(0)
    index_b = df_2.columns

    new_index = []
    for i, j in zip(index_a, index_b):
        j = j.split(".")[0]
        if "Unnamed" in i:
            new_index.append(j)
        else:
            new_index.append(i + j)
        pass
    df_2.columns = new_index

    global cn_report
    cn_report = df_2


def search_company(path):
    """
    查找公司所在管辖行
    :param path: excel
    :return: 统计结果
    """
    # 报备客户底表处理多级表头
    new_column_maker(path)
    global cn_report
    cn_report = cn_report.rename(columns={"上市公司（含拟上市）高管客户营销报备汇总表序号": "序号", "上市公司（含拟上市）高管客户营销报备汇总表管辖行": "管辖行（实际）",
                                          "上市公司（含拟上市）高管客户营销报备汇总表客户姓名": "客户姓名", "上市公司（含拟上市）高管客户营销报备汇总表公司全称": "公司全称",
                                          "上市公司（含拟上市）高管客户营销报备汇总表晋级层级": "晋级层级"})
    # cn_report.to_excel("多级表头处理后.xlsx")
    cn_report = cn_report.drop(["上市公司（含拟上市）高管客户营销报备汇总表网点 "], axis=1)

    # 将公司总表的index换成“公司中文名称”
    global cn_company
    index_list = cn_company["公司中文名称"].values.tolist()
    cn_company.set_index("公司中文名称", inplace=True, drop=True)
    # print(cn_company)

    # 报备客户底表增加列名
    col_name = cn_report.columns.tolist()
    col_name.insert(len(col_name), "管辖行（建议）")
    cn_report = cn_report.reindex(columns=col_name)

    for index, row in cn_report.iterrows():
        if cn_report.loc[index, "公司全称"] in index_list:
            cn_report.loc[index, "管辖行（建议）"] = cn_company.loc[cn_report.loc[index, "公司全称"], "管辖行"]
        else:
            cn_report.loc[index, "管辖行（建议）"] = ""

    # 双重循环
    # for index, row in cn_report.iterrows():
    #     for index1, row1 in cn_company.iterrows():
    #         if cn_report.loc[index, "上市公司（含拟上市）高管客户营销报备汇总表公司全称"] == cn_company.loc[index1, "公司中文名称"]:
    #             cn_report.loc[index, "公司管辖行"] = cn_company.loc[index1, "管辖"]


if __name__ == '__main__':
    file_path = r".\原数据.xlsx"

    # 公司总表
    cn_company = pd.read_excel(open(file_path, 'rb'), sheet_name="公司总表")

    # 统计公司总表
    require_company = compute_require_company(cn_company)
    # require_company.to_excel("公司统计.xlsx")

    # 制作报备客户核实表
    search_company(file_path)
    # cn_report.to_excel("报备客户核实.xlsx")

    # 个人客户去重
    cn_individual = pd.read_excel(open(file_path, 'rb'), sheet_name="个人客户总表")

    # location_list = cn_individual["客户归属支行"]
    # for location in location_list:
    #     if location != "市分行营业部" and location:
    #         location_result = location.replace("支行", "", 1)
    #         location_result = location_result.replace("分行", "", 1)
    # cn_individual["客户归属支行"] = location_list

    cn_individual["true or false"] = cn_individual["管辖行（建议）"] == cn_individual["客户归属支行"]
    cn_individual = cn_individual[cn_individual["true or false"] == 1]
    # cn_individual.to_excel("个人用户核实.xlsx")
    drop_individual = cn_individual.drop_duplicates(subset=["公司"], keep="first")
    # cn_individual.to_excel("个人用户核实（去重）.xlsx")

    # 报备客户去重
    cn_report["true or false"] = cn_report["管辖行（实际）"] == cn_report["管辖行（建议）"]
    cn_report = cn_report[cn_report["true or false"] == 1]
    # cn_report.to_excel("报备用户核实.xlsx")
    # drop_report = cn_report.drop_duplicates(subset=["公司全称"], keep="first")

    # 改列头
    cn_report = cn_report.rename(columns={"公司全称": "公司", "晋级层级": "层级"})
    # cn_report = cn_report.drop(["管辖行（实际）"], axis=1)

    # 汇总客户
    cn_total = pd.concat([cn_individual, cn_report])
    # cn_total.to_excel("个人+报备覆盖用户.xlsx")
    drop_total = cn_total.drop_duplicates(subset=["公司"], keep="first")
    # drop_total = cn_total["公司"].drop_duplicates()
    # drop_total.to_excel("个人+报备覆盖用户（去重）.xlsx")

    completed_company = compute_completed_company(drop_total)
    # completed_company.to_excel("完成公司统计.xlsx")

    # 计算覆盖率
    df_compute = pd.merge(require_company, completed_company, left_index=True, right_index=True)
    # df_compute.to_excel("计算覆盖率.xlsx")

    # 增加列名
    col_name = df_compute.columns.tolist()
    col_name.insert(len(col_name), "公司覆盖率")
    df_compute = df_compute.reindex(columns=col_name)
    ini_tf = np.zeros((df_compute.shape[0], 1))
    df_compute["公司覆盖率"] = ini_tf

    for index, row in df_compute.iterrows():
        x = df_compute.loc[index, "计数项:公司个数"]
        y = df_compute.loc[index, "公司"]
        if x != 0:
            df_compute.loc[index, "公司覆盖率"] = str(round(y / x, 2)*100) + "%"
        else:
            df_compute = df_compute.drop(index=index)
    # df_compute = df_compute.rename(columns={"计数项:公司个数_y": "开户数", "计数项:公司个数_x": "公司数"})

    # 筛选高净值
    # 合并总表
    cn_report = cn_report.rename(columns={"公司全称": "公司", "晋级层级": "层级"})
    cn_report = cn_report.drop(["管辖行（实际）"], axis=1)
    cn_total_pick = pd.concat([cn_individual, cn_report])

    cn_total_pick.reset_index(drop=True, inplace=True)

    # 筛选高净值
    for index, row in cn_total_pick.iterrows():
        if row["层级"] != "私行1" and row["层级"] != "私行2" and row["层级"] != "理财" and row["层级"] != "财富":
            cn_total_pick = cn_total_pick.drop(index=index)
    # cn_total_pick.to_excel("个人+报备高净值用户.xlsx")

    # 公司去重
    cn_total_pick = cn_total_pick.drop_duplicates(subset=["公司"], keep="first")

    # 统计
    value_customer = compute_completed_company(cn_total_pick)

    # 统计总表
    compute_output = pd.merge(df_compute, value_customer, left_index=True, right_index=True)

    # 按公司覆盖率排序
    compute_output = compute_output.sort_values(by=["公司覆盖率"], ascending=False)

    # 增加列名
    col_name = compute_output.columns.tolist()
    col_name.insert(len(col_name), "高净值覆盖率")
    compute_output = compute_output.reindex(columns=col_name)
    ini_tf = np.zeros((compute_output.shape[0], 1))
    compute_output["高净值覆盖率"] = ini_tf

    # 计算高净值覆盖率
    for index, row in compute_output.iterrows():
        y = compute_output.loc[index, "公司_y"]
        x = compute_output.loc[index, "计数项:公司个数"]
        if x != 0:
            compute_output.loc[index, "高净值覆盖率"] = str(round(y / x, 2)*100) + "%"
        else:
            compute_output = compute_output.drop(index=index)

    # 统计总计
    little_sum = compute_output.sum()
    compute_output.loc["总计"] = little_sum

    compute_output = compute_output.rename(columns={"计数项:公司个数": "指标公司数", "公司_x": "覆盖公司数", "公司_y": "高净值公司数"})
    xx = compute_output.loc["总计", "指标公司数"]
    yy = compute_output.loc["总计", "覆盖公司数"]
    zz = compute_output.loc["总计", "高净值公司数"]
    compute_output.loc["总计", "公司覆盖率"] = str(round(yy / xx, 2) * 100) + "%"
    compute_output.loc["总计", "高净值覆盖率"] = str(round(zz / xx, 2) * 100) + "%"

    compute_output.to_excel("output.xlsx")

