import pymysql

conet=pymysql.connect(host='192.168.0.01',port=3306,user='root',passwd='root',db='test_db',charset='utf8')
cursor=conet.cursor()
cursor.execute("select * from user")
result = cursor.fetchall()
cursor.close()
conet.close()