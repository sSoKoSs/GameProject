import SQLCon
import os


def main():
    #TODO check for config to auto load Name

    print "Welcome to this roguelike (the game is not fun its just to test out the sql database)"
    awnser = raw_input("(L)ogin or (R)egister > ")
    if awnser == "L" or awnser == "l":
        pass #TODO complete the login system

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


if __name__ == '__main__':
    main()

    # import the main game and start it
    import Main
    Main.main()
