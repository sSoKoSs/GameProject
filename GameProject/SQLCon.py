import mysql.connector

cnx = mysql.connector.connect(user='root', password='123qwe', database='gamedb')
cursor = cnx.cursor()

###TODO make the getName func TODO###

###TODO make the getPassword func TODO###

###TODO make the getStats for all of the objects func TODO###


###TODO make the submitName / Password func TODO###

###TODO make the setLevelIDForPlayer func TODO###

def getMapDataForID(userID):
    map = []
    ListStart=0
    ListEnd=25

    query = ("SELECT data FROM level INNER JOIN user ON user.level_ID = level.ID where user.id = " + str(userID))
    cursor.execute(query)

    data = str(cursor.fetchall())[4:-4]
    # parse the data to a 2D array
    for y in xrange(23):
        map.append(data[ListStart:ListEnd])
        ListStart, ListEnd = ListEnd, ListStart+50
    return map

# map = getMapDataForID(1)
# for line in map:
#     print line




for result in cursor:
  print result

cursor.close()
cnx.close()
