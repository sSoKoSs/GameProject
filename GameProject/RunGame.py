import SQLCon
import os


sqlcon = SQLCon.sqlcon()

def main():
    #TODO check for config to auto load Name

    print "Welcome to this roguelike (the game is not fun its just to test out the sql database)"
    awnser = raw_input("(L)ogin or (R)egister > ")
    if awnser == "L" or awnser == "l":
        os.system("cls")
        while True:
            print "Login here."
            name = raw_input("Name > ")
            password = raw_input("Password > ")
            os.system("cls")

            result, userID = sqlcon.searchNamesForID(name)
            if result:
                if password == sqlcon.getPasswordForID(userID):
                    startGame(userID)
                    break
            os.system("cls")
            print "Wrong credentials. Try again"


    else:
        os.system("cls")
        print "Register below."

        while True:
            name = raw_input("Name > ")

            #TODO check if name is taken

            password = raw_input("Password > ")
            #validation
            if(password != raw_input("Re-enter Password > ")):
                os.system("cls")
                print "wrong password try again"
                print "Register below."
                continue
            break

            #TODO update the User table with the new user

def startGame(userID):
    sqlcon.endConnection()
    # import the main game and start it
    import Main
    Main.main(userID)


if __name__ == '__main__':
    main()
