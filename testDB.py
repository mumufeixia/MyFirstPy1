#!/usr/bin/python
# -*- coding:utf8 -*-
import MySQLdb

'''
DROP TABLE IF EXISTS EMPLOYEE
CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )        
INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)         
SELECT * FROM EMPLOYEE WHERE INCOME > 1000
UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = M " 
DELETE FROM EMPLOYEE WHERE AGE > 20

'''

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "0", "Test", charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("show databases;")

# # 创建数据表SQL语句
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
#          LAST_NAME, AGE, SEX, INCOME)
#          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
#
# sql = "SELECT * FROM EMPLOYEE \
#        WHERE INCOME > '%d'" % (1000)

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchall()

print data
# cursor.execute(sql)

# 关闭数据库连接
db.close()