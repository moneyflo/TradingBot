import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='stock_1',
                             user='root', passwd='********', autocommit=True)
# autocommit=True로 해주면 따로 commit() 함수를 호출하지 않아도됨.

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()  # execute의 결과값을 튜플로 반환

print(f"MariaDB version : {result}")

connection.close()
