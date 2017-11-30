import SQLCon
import os


sqlcon = SQLCon.sqlcon()

def main():
    print "Welcome to this roguelike (the game is not fun its just to test out the sql database)"
    awnser = raw_input("(L)ogin or (R)egister or (A)utoLogin > ")

    #This checks and reads the config.txt to get the id and start the game
    if awnser == "A" or awnser == "a":
        try:
            conf = open("config.txt","r")
            UserID = conf.read()
            conf.close()
            startGame(UserID)
            return
        except:
            awnser = "NLY"

    if awnser == "L" or awnser == "l" or awnser == "NLY":
        os.system("cls")
        if awnser == "NLY":
            print "You haven't logged/registered in yet."

        while True:
            print "Login here."
            name = raw_input("Name > ")
            password = raw_input("Password > ")
            os.system("cls")

            #result returns true if the <name> is in the database
            result, userID = sqlcon.searchNamesForID(name)
            if result:
                if password == sqlcon.getPasswordForID(userID):
                    autoConnect(userID)
                    startGame(userID)
                    return
            os.system("cls")
            print "Wrong credentials. Try again"


    else:
        os.system("cls")
        print "Register below."

        while True:
            name = raw_input("Name > ")

            result, id = sqlcon.searchNamesForID(name)
            if result:
                os.system("cls")
                print "name taken try another"
                continue

            password = raw_input("Password > ")
            #validation
            if(password != raw_input("Re-enter Password > ")):
                os.system("cls")
                print "wrong password try again"
                print "Register below."
                continue

            sqlcon.newUser(name, password)
            UserID = sqlcon.sqlQuery("SELECT ID from User WHERE Name='%s'" % name)
            sqlcon.sqlPost("INSERT INTO Player (MaxHP, CurrentHP, PotisionX, PotisionY, Attack, Defence, User_ID) VALUES (10, 10, 1, 1, 3, 1, %s)" % UserID)
            main() # to login again (just to make sure)
            return

#Makes the config.txt file and saves the current logged or registered ID
def autoConnect(UserID):
    print "Do you want to auto-join the next time? (y/n)"
    auto = raw_input("Auto > ")

    if auto == "y" or auto == "Y":
        with open("config.txt","w") as conf:
            conf.write(str(UserID))
        print "created conf.txt"

def startGame(userID):
    sqlcon.endConnection()
    # import the main game and start it
    import Main
    Main.main(userID)


if __name__ == '__main__':
    main()
