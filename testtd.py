import rpa as r
import UrlModel as um


def edge_on():
    '''
    浏览器启动
    :return:
    '''
    r.tagui_location(r"D:\pycharm")
    r.init()

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

def mainmember_distinguish_xpath():
    '''
    获取数量
    '''
    xpath_shareholder_1 = '''//*[@id="mainmember"]/div[2]/div[2]/table/tr/td[2]/div/span[2]/span[1]/a'''
    xpath_shareholder_2 = '''//*[@id="mainmember"]/div[3]/div[2]/table/tr/td[2]/div/span[2]/span[1]/a'''

    num1 = r.count(xpath_shareholder_1)
    num2 = r.count(xpath_shareholder_2)
    print('!!!!!')
    print(num1)
    print(num2)
    num_result = max(int(num1), int(num2))
    return num_result

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


def get_executive():
    '''
    :return: [ ["顾敏","董事长,法定代表人"], ["李南青","总经理,董事"] ]
    '''
    # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td.left > div > span.cont > span > a
    num = mainmember_distinguish_xpath()  # if num = 5 [ [],[],[],[],[],
    print(num)
    if num != 0:
        result = []
        # #mainmember > div:nth-child(2) > div.app-ntable > table > tr:nth-child(2) > td:nth-child(5) > span
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

edge_on()
um.go_href('https://www.qcc.com/firm/b975f62a505755c624c9b9098a33bf05.html')
css = executive_distinguish()
print(css)
print(get_executive())
print(r.read('#mainmember > div.tablist > div.tcaption > span.title-tab > span:nth-child(1) > a > span.tbadge'))

x =  ['300', '301', '324', '336', '347', '348', '345', '346', '359', '370']
y = [x for i in x int(i)+3]