# 界面文件为 ShowWindow.py
import pymysql
from PyQt5.Qt import *
import sys
# coding=utf-8
import re
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow, QApplication
# 继承至界面文件的主窗口类
# encoding=utf-8
from QT.ShowWindow import Ui_MainWindow
import jieba
# 用于连接数据库
config = {
    "host": "47.102.223.103",
    "port": 3306,
    'database': 'course_design',
    "charset": "utf8",
    "user": "root",
    "password": "aliyun"
}

class MyMainWindow(QMainWindow, Ui_MainWindow):

    """
    构造函数初始化
    连接数据库
    加载自定义词典库
    Attributes:
        self.db: 连接数据库
        self.cur：与数据库建立的连接关系
        self.model:表格模型，与UI界面的表格绑定，用于显示信息
    """
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # 触发函数确定按钮，重置按钮
        self.Ok_But.clicked.connect(self.on_Ok_But_click)
        self.Reset_But.clicked.connect(self.on_Reset_But_click)
        # 连接数据库
        self.db = pymysql.connect(**config)
        self.cur = self.db.cursor()
        # 加载jieba自定义词典
        jieba.load_userdict("dictionary.txt")
        # 为表格显示做准备
        self.model = QStandardItemModel()

    '''
    添加查询报错相应机制(详细报错)
    TODOOOOOOOOOOOOO设置窗口关闭时断开数据库连接
    
    执行SQL语句在数据库中获得结果
    Args:
        sql:要执行的SQL语句
    Returns:
        results:查询的结果
        -1：当执行出错时返回标识符-1
    Raises:
        EXception:以防万一，一旦出现任何错就报错。
    '''
    def search(self, sql):
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            return results
        except Exception:
            return -1

    '''
    获取列名
    Returns:
        colname:列名列表
        -1：出错标识符-1
    Raises:
        Exception:以防万一，出现任何错都报错 
    '''
    def get_colname(self):
        try:
            colname = [tup[0] for tup in self.cur.description]  # 获得列名
            return colname
        except Exception:
            return -1

    '''
    获取输入的自然语言和SQL语句
    Attributes:
        self.wquery:输入的自然语言
        self.sqlquery:输入的SQL语句
    '''
    def get_input(self):
        self.wquery = self.InQ_Text.toPlainText()      # 获取输入的自然语言
        self.sqlquery = self.InSql_Text.toPlainText()  # 获取sql语句

    '''
    使用jieba分词对自然语言进行分词
    '''
    def solvewkeys(self):
        self.wkey = jieba.lcut(self.wquery)  #  对输入的自然语言进行分词
        # print(self.wkey)

    '''
    输入参数清空/重置
    '''
    def init_input(self):
        self.wquery = ""     # 清空输入的自然语言
        self.Sqlquer = ""    # 清空输入的SQL语句
        self.model.clear()   # 清空上一次查询的结果

    '''
    根据输入的SQL语言对比数据库查询函数
    并把结果显示到表格
    Attributes:
        self.rowsum:结果集（表格显示）总行数
        self.colsum:结果集（表格显示）总列数
    '''
    def search_sql(self):
        # 执行对应的查询命令
        data = self.search(self.sqlquery)
        # 查询异常
        if(data == -1):
            print(QMessageBox.information(self, "提醒", "数据库查询出错！", QMessageBox.Yes, QMessageBox.Yes))
            return
        self.rowsum = len(data)  # 总行数
        # 查询无结果
        if (self.rowsum == 0):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            return

        self.colsum = len(data[0])  # 总列数
        # 获得列名
        colname = self.get_colname()
        # 获取列名失败
        if(colname == -1):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            return
        self.model.setHorizontalHeaderLabels(colname)       # 设置列名
        f = open('document.txt', mode='w', encoding='utf-8')

        for i in range(self.rowsum):
            for j in range(self.colsum):
                tempdata = data[i][j]
                finaldata = QStandardItem(str(tempdata))
                if i < 1000:
                    self.model.setItem(i, j, finaldata)
                f.write(str(tempdata)+" ")
            if i < 1000:
                self.SearchRes_Tab.setModel(self.model)   # 结果插入表
            f.write("\n")
    '''
    对test测试的内容进行错误检验
    '''
    def test1check(self,a):
        for i in range(len(a)):
            flag=0
            for j in range(len(self.wkey)):
                if(a[i] in self.wquery):
                    flag = 1
                    break
                if (self.wkey[j]==a[i]):
                    flag=1
                    break
            if(flag==0):
                print(QMessageBox.information(self, "提醒", "自然语言中没有'"+a[i]+"'关键词", QMessageBox.Yes, QMessageBox.Yes))
                return 0
        return 1

    def test1(self, natureLanguage, sqlLanguage):
        # 按照空格将sqlLanguage中的单词分隔开
        sqlkey = sqlLanguage.split(" ")

        # 构造两个列表,顺序相同,用于记录那个
        '''
        a存储where中的列名
        b存储where中列名的关键字
        c中存储的为连接条件中前面的列名
        d中存储的为连接条件后免得列名或关键字
        a,b一一对应  c,d一一对应
        '''
        a = []
        b = []
        c = []
        d = []
        for index in range(len(sqlkey)):
            if re.compile(r"'(.*?)'").findall(sqlkey[index]):
                a.append(sqlkey[index - 2])
                b.append(re.compile(r"'(.*?)'").findall(sqlkey[index])[0])
            else:
                if sqlkey[index - 1] == '=':
                    c.append(sqlkey[index - 2])
                    d.append(sqlkey[index])
        # 进行错误检验 对sql语句合自然语言
        if self.test1check(b)==0:
            return
        self.search_sql()  # 执行查询并显示到表格
        # 输出特定列,按照a中的顺序进行添加
        sql = "select distinct "
        for index in range(len(a) - 1):
            sql = sql + a[index] + " , "
        if len(a) > 0:
            sql = sql + a[len(a) - 1] + " from "
        if len(a) == 0:
            sql = sql + "* "

        sql = sql + re.compile(r"from (.*?) where").findall(sqlLanguage)[0]
        if len(c) > 0:
            sql = sql + " where "
        print(sql)
        for index in range(len(c) - 1):
            sql = sql + c[index] + " = " + d[index] + " and "
        # print(sql)
        if len(c) > 0:
            sql = sql + c[len(c) - 1] + " = " + d[len(c) - 1]
        # print(sql)
        db = pymysql.connect(**config)
        cur = db.cursor()
        cur.execute(sql)
        k = 0
        self.model1 = QStandardItemModel()
        self.model2 = QStandardItemModel()
        f = open('sqlnat.txt', mode='w', encoding='utf-8')
        d=0
        for i in cur.fetchall():  # i为一个列表
            a1 = natureLanguage
            b1 = sqlLanguage
            for j in range(len(i)):
                a1 = a1.replace(b[j], i[j])
                b1 = b1.replace(b[j], i[j])
            if d<1000:
                self.model1.setItem(k, 0, QStandardItem(str(a1)))
                self.model2.setItem(k, 0, QStandardItem(str(b1)))
            f.write(str(a1)+"\n")
            f.write(str(b1) + "\n")
            # print(a1)
            # print(b1)
            k = k+1
            if d<1000:
                self.SonQ_Tab.setModel(self.model1)
                self.SonSQL_Tab.setModel(self.model2)
            d=d+1

    def test2(self, natureLanguage, sqlLanguage):
        self.search_sql()  # 执行查询并显示到表格
        # 按照空格将sqlLanguage中的单词分隔开
        sqlkey = sqlLanguage.split(" ")
        # 创建一个字典 存放表中列名(中文)和列名(英文)其中key;表名+1(自然语言中的列名),表名+2(sql语言中的列名)
        # sqlTab字典用于存放不同表中的列
        sqlTab = dict()
        sqlTab["province"] = ["province.p_id", "province.p_name"]
        sqlTab["schools"] = ["schools.s_id", "schools.s_name"]
        sqlTab["majors"] = ["majors.m_id", "majors.m_name", "majors.batch"]
        sqlTab["province_line"] = ["province_line.p_id", "province_line.year", "province_line.type",
                                   "province_line.batch", "province_line.line"]
        sqlTab["school_line2016"] = ["school_line2016.s_id", "school_line2016.p_id", "school_line2016.type",
                                   "school_line2016.batch", "school_line2016.average", "school_line2016.lowest",
                                   "school_line2016.province_line"]
        sqlTab["school_line2017"] = ["school_line2017.s_id", "school_line2017.p_id", "school_line2017.type",
                                     "school_line2017.batch", "school_line2017.average", "school_line2017.lowest",
                                     "school_line2017.province_line"]
        sqlTab["school_line2018"] = ["school_line2018.s_id", "school_line2018.p_id", "school_line2018.type",
                                     "school_line2018.batch", "school_line2018.average", "school_line2018.lowest",
                                     "school_line2018.province_line"]
        sqlTab["major_line2016"] = ["major_line2016.s_id", "major_line2016.m_id", "major_line2016.p_id",
                                    "major_line2016.type", "major_line2016.batch", "major_line2016.average",
                                    "major_line2016.lowest"]
        sqlTab["major_line2017"] = ["major_line2017.s_id", "major_line2017.m_id", "major_line2017.p_id",
                                    "major_line2017.type", "major_line2017.batch", "major_line2017.average",
                                    "major_line2017.lowest"]
        sqlTab["major_line2018"] = ["major_line2018.s_id", "major_line2018.m_id", "major_line2018.p_id",
                                    "major_line2018.type", "major_line2018.batch", "major_line2017.average",
                                    "major_line2018.lowest"]
        sqlLan = dict()
        sqlLan["province.p_id"] = ["省号"]
        sqlLan["province.p_name"] = ["省名"]
        sqlLan["schools.s_id"] = ["学校号"]
        sqlLan["schools.s_name"] = ["学校名"]
        sqlLan["majors.m_id"] = ["专业号"]
        sqlLan["majors.m_name"] = ["专业名"]
        sqlLan["majors.batch"] = ["专业批次"]
        sqlLan["province_line.p_id"] = ["省号"]
        sqlLan["province_line.year"] = ["年份"]
        sqlLan["province_line.type"] = ["类别"]
        sqlLan["province_line.batch"] = ["批次"]
        sqlLan["province_line.line"] = ["省分数线"]
        sqlLan["school_line2016.s_id"] = ["学校号"]
        sqlLan["school_line2016.p_id"] = ["省号"]
        sqlLan["school_line2016.type"] = ["类别"]
        sqlLan["school_line2016.batch"] = ["批次"]
        sqlLan["school_line2016.average"] = ["平均分"]
        sqlLan["school_line2016.lowest"] = ["最低分"]
        sqlLan["school_line2016.province_line"] = ["省分数线"]
        sqlLan["school_line2017.s_id"] = ["学校号"]
        sqlLan["school_line2017.p_id"] = ["省号"]
        sqlLan["school_line2017.type"] = [";类别"]
        sqlLan["school_line2017.batch"] = ["批次"]
        sqlLan["school_line2017.average"] = ["平均分"]
        sqlLan["school_line2017.lowest"] = ["最低分"]
        sqlLan["school_line2017.province_line"] = ["省分数线"]
        sqlLan["school_line2018.s_id"] = ["学校号"]
        sqlLan["school_line2018.p_id"] = ["省号"]
        sqlLan["school_line2018.type"] = [";类别"]
        sqlLan["school_line2018.batch"] = ["批次"]
        sqlLan["school_line2018.average"] = ["平均分"]
        sqlLan["school_line2018.lowest"] = ["最低分"]
        sqlLan["school_line2018.province_line"] = ["省分数线"]
        sqlLan["major_line2016.s_id"] = ["学校号"]
        sqlLan["major_line2016.m_id"] = ["专业号"]
        sqlLan["major_line2016.p_id"] = ["省号"]
        sqlLan["major_line2016.type"] = ["类别"]
        sqlLan["major_line2016.batch"] = ["批次"]
        sqlLan["major_line2016.average"] = ["平均分"]
        sqlLan["major_line2016.lowest"] = ["最低分"]
        sqlLan["major_line2017.s_id"] = ["学校号"]
        sqlLan["major_line2017.m_id"] = ["专业号"]
        sqlLan["major_line2017.p_id"] = ["省号"]
        sqlLan["major_line2017.type"] = ["类别"]
        sqlLan["major_line2017.batch"] = ["批次"]
        sqlLan["major_line2017.average"] = ["平均分"]
        sqlLan["major_line2017.lowest"] = ["最低分"]
        sqlLan["major_line2018.s_id"] = ["学校号"]
        sqlLan["major_line2018.m_id"] = ["专业号"]
        sqlLan["major_line2018.p_id"] = ["省号"]
        sqlLan["major_line2018.type"] = ["类别"]
        sqlLan["major_line2018.batch"] = ["批次"]
        sqlLan["major_line2018.average"] = ["平均分"]
        sqlLan["major_line2018.lowest"] = ["最低分"]
        self.model3 = QStandardItemModel()
        self.model4 = QStandardItemModel()

        for i in range(len(sqlTab[str(sqlkey[4])])):
            lan = natureLanguage
            sqlen = sqlLanguage
            # a为根据sql语句中的列名,找到他的中文名
            a = sqlLan[str(sqlkey[2])][0]
            lan = lan.replace(str(a), sqlLan[str(sqlTab[str(sqlkey[4])][i])][0])
            sqlen = sqlen.replace(str(sqlkey[2]), sqlTab[str(sqlkey[4])][i])
            self.model3.setItem(i, 0, QStandardItem(str(lan)))
            self.model4.setItem(i, 0, QStandardItem(str(sqlen)))
            print(lan)
            print(sqlen)
        self.SonQ_Tab.setModel(self.model3)
        self.SonSQL_Tab.setModel(self.model4)
    # **************************************************************
    def sub(self,str, p, c):  # 替换str中某一位置的字符
        new = []
        for s in str:
            new.append(s)
        new[p] = c
        str = ''.join(new)
        return str
        # print(str)

    def deletedouhao(self,str):  # 删除逗号前后的空格
        start1 = 0
        position = str.find(",", start1)
        a = []
        while position > -1:  # jsfs, d
            # print(position)  #jsfs,d
            if str[position - 1: position] == " ":
                str = self.sub(str, position - 1, '')
                position = position - 1
                if str[position + 1: position + 2] == " ":
                    str = self.sub(str, position + 1, '')
                    start1 = position + 1
                else:
                    start1 = position + 1
            else:
                if str[position + 1: position + 2] == " ":
                    str = self.sub(str, position + 1, '')
                    start1 = position + 1
                else:
                    start1 = position + 1
            position = str.find(",", start1)
        return str
        # print(str)

    def deletedenghao(self,str):  # 删除等号前后的空格
        start1 = 0
        position = str.find("=", start1)
        a = []
        while position > -1:  # jsfs, d
            # print(position)  #jsfs,d
            if str[position - 1: position] == " ":
                str = self.sub(str, position - 1, '')
                position = position - 1
                if str[position + 1: position + 2] == " ":
                    str = self.sub(str, position + 1, '')
                    start1 = position + 1
                else:
                    start1 = position + 1
            else:
                if str[position + 1: position + 2] == " ":
                    str = self.sub(str, position + 1, '')
                    start1 = position + 1
                else:
                    start1 = position + 1
            position = str.find("=", start1)
        return str
        # print(str)

    def InputStandard(self,str):
        str = str.replace('>=', '@')
        str = str.replace('<=', '#')
        str = self.deletedouhao(str)
        str = self.deletedouhao(str)
        str = self.deletedenghao(str)
        str = self.deletedenghao(str)
        start2 = 0
        position = str.find(",", start2)
        a = []
        while position > -1:
            # print(position)
            a.append(position)
            start2 = position + 1
            position = str.find(",", start2)

        start2 = 0
        position = str.find("=", start2)
        b = []
        while position > -1:
            # print(position)
            b.append(position)
            start2 = position + 1
            position = str.find("=", start2)
        # a = []
        # b = []
        # a = findComma(",aj=k,a=kk=jk,")
        # b = findEqulas_sign(",aj=k,a=kk=jk,")
        a.extend(b)
        a.sort()  # 数组a的值是“，”与“=”在字符串中的位置
        # print(a)
        # n = len(a)
        str1 = list(str)

        for i in range(len(a)):
            str1.insert(a[i] + 2 * i, " ")
            str1.insert(a[i] + 2 * (i + 1), " ")
        str = ''.join(str1)
        # print(str.find(",", 0, end))
        # str1 = list(str)
        # str1.insert(str.find(",", 0, 10), " ")
        # str1.insert(str.find(",", 0, 10)+2, " ")
        # str = ''.join(str1)\
        str = str.replace('@','>=')
        str = str.replace('#','<=')
        return str

    # ************************************************************************************
    '''
    查询按钮响应事件
    Attributes:
        self.rowsum:结果集（表格显示）总行数
        self.colsum:结果集（表格显示）总列数
    '''
    def on_Ok_But_click(self):
        self.init_input()  # 重置
        self.get_input()   # 获取输入的自然语言和SQL语句

        # 如果输入为空，报错处理
        if (len(self.wquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的自然语言", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (len(self.sqlquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的SQL语句", QMessageBox.Yes, QMessageBox.Yes))
            return
        self.solvewkeys()
        # self.search_sql()  # 执行查询并显示到表格
        '''
        test1用于写select from where类型的
        test2用于写select from 类型的
        test3用于写带有group by类型的
        '''
        self.sqlquery = self.InputStandard(self.sqlquery)
        print(self.sqlquery)
        if 'where' not in self.sqlquery:
            self.test2(self.wquery, self.sqlquery)
        elif 'group' in self.sqlquery:
            self.test1(self.wquery, self.sqlquery)
        else:
            self.test1(self.wquery, self.sqlquery)


    '''
    重置按钮响应事件，清空输入参数和输入显示框
    '''
    def on_Reset_But_click(self):
        # 清空输入框
        self.InSql_Text.clear()
        self.InQ_Text.clear()
        # 重置输入参数
        self.init_input()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())