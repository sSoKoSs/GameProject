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
PlayerID = -1

player = Actors.Player(Name=" ", HPMax=10, Hp=10, Attack=3, Defence=1, Coins=0, Y=12, X=12, Symbol='@')

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
    sqlcon.setLevelIDForUserID(LevelID, PlayerID)

    smap = sqlcon.getMapDataForID(PlayerID)

    makeMapObjects()
    libtcod.console_set_default_foreground(0, libtcod.lighter_grey)
    for Object in objects:
        Object.draw()

    libtcod.console_set_default_foreground(0, libtcod.green)
    for Enemy in enemies:
        Enemy.draw()


def makeLoot(x, y):
    coins.append([x, y])
    libtcod.console_set_default_foreground(0, libtcod.yellow)
    libtcod.console_put_char(0, x, y, '$', libtcod.BKGND_NONE)



def handleKeys():
    global target, playerScore, exity, exitx
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
            LevelID += 1
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
    global smap, exity, exitx
    global objects, enemies, coins, exitx, exity

    objects = []
    enemies = []
    coins = []
    exity, exitx = -1, -1

    libtcod.console_clear(0)
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print(0, 1, 24, "<v>^ : move around")

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


#############################################
# Initialization & Main Loop
#############################################
def main(userID):
    global exity, exitx

    global PlayerID
    PlayerID = userID

    global smap
    smap = []
    smap = sqlcon.getMapDataForID(PlayerID)

    global LevelID
    LevelID = sqlcon.getLevelIDforUserID(PlayerID)[0][0]
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
            pass #TODO GAME OVER

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
