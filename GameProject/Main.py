import libtcodpy as libtcod
import Actors
import SQLCon as sql

##################################### INIT #####################################
# actual size of the window
SCREEN_WIDTH = 25
SCREEN_HEIGHT = 25

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'ConsoleGame', False)

sqlcon = sql.sqlcon()
##################################### INIT #####################################

#Temporary Variables
playerScore = 0
####################
global player
global PlayerID
global target

objects = []
enemies = []
coins = []

exity, exitx = -1, -1

############## MAP ##############x25 y22 550 chars
smap = []
LevelID = -1
#################################


def changeLevel():
    global PlayerID, LevelID, smap

    libtcod.console_clear(0)
    try:
        sqlcon.setLevelIDForUserID(LevelID, PlayerID)
    except:
        LevelID = 1
        changeLevel()

    smap = sqlcon.getMapDataForID(PlayerID)

    makeMapObjects()
    libtcod.console_set_default_foreground(0, libtcod.lighter_grey)
    for Object in objects:
        Object.draw()

    libtcod.console_set_default_foreground(0, libtcod.green)
    for Enemy in enemies:
        Enemy.draw()


def postScore(score):
    sqlcon.changeScoreForUserID(score, PlayerID)

def getScore(ID):
    return sqlcon.getScoreForUserID(ID);


def makeLoot(x, y):
    coins.append([x, y])
    libtcod.console_set_default_foreground(0, libtcod.yellow)
    libtcod.console_put_char(0, x, y, '$', libtcod.BKGND_NONE)



def handleKeys():
    global target, playerScore, exity, exitx, player
    Loot = None

    key = libtcod.console_wait_for_keypress(True)  # turn-based

    playery, playerx = player.Y, player.X

    if key.vk == libtcod.KEY_ESCAPE:
        return True  # exit game

    # movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        playery -= 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1

    # key to move to another level
    if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        if player.Y == exity and player.X == exitx:
            global LevelID
            global playerScore
            LevelID += 1
            postScore(playerScore)
            changeLevel()

    if isBlocked(playerx, playery):
        #if try fails means it is not an enemy so ignore
        try:
            Loot = target.LoseHealth(player.Attack)
            player.Hp -= 1
        except:
            pass
    else:
        player.move(playerx, playery)

        # for all the coins check if player is on top if True then increase score
        for i in coins:
            if playerx == i[0] and playery == i[1]:
                #remove the coin so player won't be able to get the same coin
                coins.remove(i)
                playerScore += 1
                #clear the instructions and redraw the score there
                libtcod.console_print(0, 1, 24, "                  ")
                libtcod.console_print(0, 1, 24, "Score: %s" % playerScore)

    if Loot != None:
        #if try fails means it is not an enemy so ignore
        try:
            enemies.remove(target)
            # Loot[0] = x , Loot[1] = y
            makeLoot(Loot[0], Loot[1])
        except:
            pass


def makeMapObjects():
    global playerScore
    global smap, exity, exitx
    global objects, enemies, coins, exitx, exity

    objects = []
    enemies = []
    coins = []
    exity, exitx = -1, -1

    libtcod.console_clear(0)
    libtcod.console_set_default_foreground(0, libtcod.white)
    #don't show instructions when player has some score
    if playerScore == 0:
        libtcod.console_print(0, 1, 24, "<v>^ : move around")
    else:
        libtcod.console_print(0, 1, 24, "Score: %s" % playerScore)

    for y in xrange(SCREEN_HEIGHT-3):
        for x in xrange(SCREEN_WIDTH):
            if smap[y][x] == '#':
                objects.append(Actors.Wall(Y=y, X=x, Symbol='#', Blocks=True))
            elif smap[y][x] == 'G':
                enemies.append(Actors.Grunt(Hp=1, Attack=3, Defence=0, Loot=1, Y=y, X=x, Symbol='G', Blocks=True))
            elif smap[y][x] == '>':
                exity, exitx = y, x


def isBlocked(x, y):
    global target

    if smap[y][x] == '#':
        target = None
        return True

    for Enemy in enemies:
        if Enemy.Blocks and Enemy.X == x and Enemy.Y == y:
            target = Enemy
            return True

    return False

def resetPlayer():
    postScore(0)

    # TODO In progress look sqlcon

def gameOver():
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print(0, 9, 10, "GAMEOVER")
    libtcod.console_flush()

    resetPlayer()

    libtcod.console_wait_for_keypress(True)

#############################################
# Initialization & Main Loop
#############################################
def main(userID):
    global PlayerID
    PlayerID = userID

    global player
    # playerstats all the values ID(Primary Key) and User_ID(Fotrign Key) are useless for now
    ID, MaxHP, CurrentHP, PositionX, PositionY, Attack, Defence, User_ID = sqlcon.getPlayersStats(PlayerID)[0]
    player = Actors.Player("NAMEHERE", MaxHP, CurrentHP, Attack, Defence, 0, PositionY, PositionX, '@')
    # TODO put the name here ^^^^^^

    global exity, exitx

    global playerScore
    playerScore = getScore(PlayerID)[0][0]
    if playerScore == None:
        playerScore = 0

    global smap
    smap = []
    smap = sqlcon.getMapDataForID(PlayerID)

    global LevelID
    LevelID = 1
    changeLevel()

    libtcod.console_set_default_foreground(0, libtcod.lighter_grey)
    for Object in objects:
        Object.draw()

    libtcod.console_set_default_foreground(0, libtcod.green)
    for Enemy in enemies:
        Enemy.draw()

    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print(0, 1, 23, "HP: %s" % player.Hp)

    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, 1, 23, "       ")
        libtcod.console_print(0, 1, 23, "HP: %s" % player.Hp)

        if player.Hp <= 0:
            gameOver()
            break

        libtcod.console_print(0, exitx, exity, ">")

        player.draw()

        libtcod.console_flush()  # draws(flushes) the buffer

        player.clear()

        # handle keys and exit game if needed
        exit = handleKeys()
        if exit:
            break
    sqlcon.endConnection()


if __name__ == '__main__':
    print "Don't run this one run RunGame.py instead"
    sqlcon.endConnection()
