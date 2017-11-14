import mysql.connector

class sqlcon:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='123qwe', database='gamedb')
        self.cursor = self.cnx.cursor()


    def sqlQuery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def sqlPost(self, query):
        self.cursor.execute(query)
        self.cnx.commit()


    def searchNamesForID(self, Name):
        # example of use:
        # found(True), id = searchNamesForID("kostas")
        # if found:
        #     do stuff
        data = self.sqlQuery("SELECT Name FROM User")

        for i in data:
            #search the data for the given name
            if Name == i[0]:
                #return True , ID for the given name
                return True ,self.sqlQuery("SELECT ID FROM User WHERE Name = '%s'" % Name)[0][0]
        return False ,-1 # not found give invalid ID and False


    ########## GET FUNCTIONS ###########


    def getPasswordForID(self, userID):
        try:
            return self.sqlQuery("SELECT Password FROM User WHERE ID = %s" % userID)[0][0]
        except:
            return -1 # -1 in case the userID is not in the database


    def getMapDataForID(self, userID):
        map = []
        ListStart=0
        ListEnd=25

        # this [4:-4] is to get rid of these symbols (u' data ',) at the start and end
        data = str(self.sqlQuery("SELECT data FROM level INNER JOIN user ON user.level_ID = level.ID where user.id = %s" % userID))[4:-4]

        # parse the data to a 2D array
        for y in xrange(23):
            map.append(data[ListStart:ListEnd])
            ListStart, ListEnd = ListEnd, ListStart+50  # (0, 25) first line then swap them (25, 0) and add 50 (25, 50) to get the next line
        return map

    def getLevelIDforUserID(self, UserID):
        return self.sqlQuery("SELECT Level_ID FROM user WHERE ID=%s" % UserID)


    def getPlayerForUserID(self, UserID):
        return self.sqlQuery("SELECT * FROM Player WHERE User_ID=%s" % UserID)


    def getEnemyForLevelID(self, LevelID):
        return self.sqlQuery("SELECT * FROM Enemy WHERE Level_ID=%s" % LevelID)



    ########## SET FUNCTIONS ###########

    def newUser(self, name, password):
        self.sqlPost("INSERT INTO User (name, password, level_ID) VALUES ('%s', '%s', 1)" % (name, password))


    def setLevelIDForUserID(self, level_ID, UserID):
        self.sqlPost("UPDATE User SET level_ID = %s WHERE ID = %s" % (level_ID, UserID))


    #### END the database Connection
    def endConnection(self):
        self.cursor.close()
        self.cnx.close()
