import pymysql as mysql
def connection():
    db=mysql.connect(host='localhost',port=3306,user='root',password='12345',db='iotproject')
    cmd=db.cursor()
    return db,cmd