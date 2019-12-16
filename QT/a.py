import pymysql

config = {
    "host": "47.102.223.103",
    "port": 3306,
    'database': 'course_design',
    "charset": "utf8",
    "user": "root",
    "password": "aliyun"
}
db = pymysql.connect(**config)
cur = db.cursor()
sql="select province.p_name from province,province_line where province_line.p_id=province.p_id " \
    "and province_line.year=2016 and province_line.type='文科' and province_line.batch='本科一批' and province_line.line>=500"
cur.execute(sql)
results = cur.fetchall()
print(results)