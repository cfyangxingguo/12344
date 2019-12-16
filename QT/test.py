
def test2( natureLanguage, sqlLanguage):
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
    sqlLan["school_line2016.type"] = [";类别"]
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

    for i in range(len(sqlTab[str(sqlkey[4])])):
        lan = natureLanguage
        sqlen = sqlLanguage
        # a为根据sql语句中的列名,找到他的中文名
        a = sqlLan[str(sqlkey[2])][0]
        lan = lan.replace(str(a), sqlLan[str(sqlTab[str(sqlkey[4])][i])][0])
        sqlen = sqlen.replace(str(sqlkey[2]), sqlTab[str(sqlkey[4])][i])
        print(lan)
        print(sqlen)


if __name__ == '__main__':
    lan="查询学校号"
    sql="select distinct major_line2016.s_id from major_line2016"
    test2(lan,sql)

