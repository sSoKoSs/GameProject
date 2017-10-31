import mysql.connector

cnx = mysql.connector.connect(user='root', password='123qwe', database='gamedb')
cursor = cnx.cursor()

query = ("SELECT data FROM level")

cursor.execute(query)

for result in cursor:
  print result

cursor.close()
cnx.close()