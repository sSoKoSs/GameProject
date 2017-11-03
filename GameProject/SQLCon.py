import mysql.connector

cnx = mysql.connector.connect(user='root', password='123qwe', database='gamedb')
cursor = cnx.cursor()


def sqlQuery(query):
    cursor.execute(query)
    return cursor.fetchall()


def searchNamesForID(Name):
    # example of use:
    # found(True), id = searchNamesForID("kostas")
    # if found:
    #     do stuff
    data = sqlQuery("SELECT Name FROM User")

    for i in data:
        #search the data for the given name
        if Name == i[0]:
            #return True , ID for the given name
            return True ,sqlQuery("SELECT ID FROM User WHERE Name = '%s'" % Name)[0][0]
    return False ,-1 # not found give invalid ID and False


########## GET FUNCTIONS ###########


def getPasswordForID(userID):
    try:
        return sqlQuery("SELECT Password FROM User WHERE ID = %s" % userID)[0][0]
    except:
        return -1 # -1 in case the userID is not in the database


def getMapDataForID(userID):
    map = []
    ListStart=0
    ListEnd=25

    # this [4:-4] is to get rid of these symbols (u' data ',) at the start and end
    data = str(sqlQuery("SELECT data FROM level INNER JOIN user ON user.level_ID = level.ID where user.id = %s" % userID))[4:-4]

    # parse the data to a 2D array
    for y in xrange(23):
        map.append(data[ListStart:ListEnd])
        ListStart, ListEnd = ListEnd, ListStart+50  # (0, 25) first line then swap them (25, 0) and add 50 (25, 50) to get the next line
    return map


def getPlayerForUserID(UserID):
    return sqlQuery("SELECT * FROM Player WHERE User_ID=%s" % UserID)


def getEnemyForLevelID(LevelID):
    return sqlQuery("SELECT * FROM Enemy WHERE Level_ID=%s" % LevelID)


########## SET FUNCTIONS ###########


def newUser(name, password):
    cursor.execute("INSERT INTO User (name, password, level_ID) VALUES ('%s', '%s', 1)" % (name, password))
    cnx.commit()


def setLevelIDForUserID(UserID, level_ID):
    cursor.execute("UPDATE User SET level_ID = %s WHERE ID = %s" % (level_ID, UserID))
    cnx.commit()


#newUser("htnsio", "1234567890")
#print setLevelIDForUserID(1,2)
#print sqlQuery("select * from User")
#print "UPDATE User SET level_ID = %s WHERE ID = %s" % (5, 2)
# map = getMapDataForID(1)
# for line in map:
#     print line

def endConnection():
    cursor.close()
    cnx.close()

endConnection()
