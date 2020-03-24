'''
不用了
'''

import pymysql
import pandas as pd
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='flasktest', port=3306, charset='utf8')
cur=conn.cursor()
def addUser(username,password):
    sql = "insert into user (username,password) values ('%s','%s')"%((username,password))
    cur.execute(sql)
    conn.commit()
    conn.close()

def isExisted(username,password):#判断用户名是否存在于数据库中
    sql="select * from user where username='%s' and password='%s'"%(username,password)
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)==0:
        return False
    else:
        return True