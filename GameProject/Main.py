import libtcodpy as libtcod
import Actors
import SQLCon as sql
import random
import Effects

# TODO make damage incications

##################################### INIT #####################################
# actual size of the window
SCREEN_WIDTH = 25
SCREEN_HEIGHT = 25

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'ConsoleGame', False)

sqlcon = sql.sqlcon()
##################################### INIT #####################################

global playerScore
global player
global PlayerID
global target

playerScore = 0

objects = []
enemies = []
coins = []
potions = []

exity, exitx = -1, -1

############## MAP ##############x25 y22 550 chars
smap = []
LevelID = -1
levelChange = False
#################################


def changeLevel(level_ID):
    global PlayerID, LevelID, smap

    libtcod.console_clear(0)
    try:
        if level_ID:
            LevelID = level_ID
        sqlcon.setLevelIDForUserID(LevelID, PlayerID)
    except:
        changeLevel(1)

    smap = sqlcon.getMapDataForID(PlayerID)

    makeMapObjects()
    libtcod.console_set_default_foreground(0, libtcod.lighter_grey)
    for Object in objects:
        Object.draw()

    libtcod.console_set_default_foreground(0, libtcod.green)
    for Enemy in enemies:
        Enemy.draw()

    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print(0, 1, 22, "%s" % player.Name) #Name of the player
    libtcod.console_print(0, 15, 23, "Atk: %s" % player.Attack) #Attack points
    libtcod.console_print(0, 15, 24, "Def: %s" % player.Defence) #Defence points


def postScore(score):
    sqlcon.changeScoreForUserID(score, PlayerID)

def getScore(ID):
    return sqlcon.getScoreForUserID(ID);


def makeLoot(x, y):
    # TODO make the RNG better
    # FIXME when items get on top of eachother they don't get redrawn + you get only the top item
    item = random.randint(0,1)

    if item == 0:
        #if 0 then make a coin
        coins.append([x, y])
        libtcod.console_set_default_foreground(0, libtcod.yellow)
        libtcod.console_put_char(0, x, y, '$', libtcod.BKGND_NONE)
    else:
        #else make a potion
        potions.append([x, y])
        libtcod.console_set_default_foreground(0, libtcod.red)
        libtcod.console_put_char(0, x, y, '&', libtcod.BKGND_NONE)


def handleKeys():
    global  playerScore, exity, exitx, player, PlayerID

    global levelChange
    levelChange = False

    key = libtcod.console_wait_for_keypress(True)  # turn-based

    playery, playerx = player.Y, player.X

    if key.vk == libtcod.KEY_ESCAPE:
        # When player exits save some stats
        postScore(playerScore)
        sqlcon.setPlayerStats(player.HPMax, player.Hp, player.Attack, player.Defence, PlayerID)
        # TODO Make this vvv to be in the setPlayerStats function !!!
        sqlcon.sqlPost("UPDATE player SET PositionY=%s, PositionX=%s WHERE User_ID=%s" % (player.Y, player.X, PlayerID))
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

            levelChange = True

            LevelID += 1
            postScore(playerScore)
            sqlcon.setPlayerStats(player.HPMax, player.Hp, player.Attack, player.Defence, PlayerID)
            changeLevel(LevelID)

    handleCollisionWithObjects(playerx, playery)


def handleCollisionWithObjects(playerx, playery):
    global target, playerScore

    Loot = None

    if isBlocked(playerx, playery):
        #if try fails means it is not an enemy so ignore
        try:
            enDamage = player.Attack - target.Defence
            if enDamage < 1:
                enDamage = 1
            Loot = target.LoseHealth(player.Attack)

            # TODO make the damage more based on the difficulty: * difficulty <-- (do this) or make the enemies stats better***
            damage = target.Attack - player.Defence
            # this is to make sure the player takes at least 1 damage and doesn't heal from enemie blows
            if damage < 1:
                damage = 1
            player.Hp -= damage

            # TODO make the damage effect here
            playerDamageText = Effects.text(player.X, player.Y-1, str(damage))
            playerDamageText.play()
        except:
            pass
    else:
        player.move(playerx, playery)

        # for all the coins check if player is on top if True then increase score
        for i in coins:
            if playerx == i[0] and playery == i[1]:
                #remove the coin so player won't be able to get the same coin
                coins.remove(i)
                playerScore += random.randint(1,5)
                #clear the instructions and redraw the score there
                libtcod.console_print(0, 1, 24, "            ")
                libtcod.console_print(0, 1, 24, "Score: %s" % playerScore)

        for i in potions:
            if playerx == i[0] and playery == i[1]:
                #remove the coin so player won't be able to get the same coin
                potions.remove(i)
                player.Hp += random.randint(2,5)
                #don't make the current health more than the max health points
                if player.Hp > player.HPMax:
                    player.Hp = player.HPMax

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
                enemies.append(Actors.Grunt(Hp=5, Attack=3, Defence=0, Loot=1, Y=y, X=x, Symbol='G', Blocks=True))
            elif smap[y][x] == '>':
                exity, exitx = y, x
            elif smap[y][x] == '@':
                player.Y = y
                player.X = x


def isBlocked(x, y, isEnemy=False):
    global target

    if smap[y][x] == '#':
        target = None
        return True

    for Enemy in enemies:
        if Enemy.Blocks and Enemy.X == x and Enemy.Y == y:
            target = Enemy
            return True

    if isEnemy and player.X == x and player.Y == y:
            return True

    return False

def resetPlayer():
    global PlayerID

    postScore(0)
    changeLevel(1)
    sqlcon.setPlayerStats(10, 10, 3, 1, PlayerID)

def gameOver():
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print(0, 9, 10, "GAMEOVER")
    libtcod.console_flush()

    resetPlayer()

    libtcod.console_wait_for_keypress(True)

    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print(0, 9, 11, "You died")
    libtcod.console_flush()

    libtcod.console_wait_for_keypress(True)

def moveEnemies():
    global enemies

    for enemy in enemies:
        decision = random.randint(0,1)
        ymove = 0
        xmove = 0

        # for Y movement calculate where to go
        if enemy.Y < player.Y:
            ymove += 1
        else:
            ymove -= 1

        # for X movement calculate where to go
        if enemy.X < player.X:
            xmove += 1
        else:
            xmove -= 1

        # TODO make this better and smaller

        # if 0 and you can move then move on the Y axis else move on X if you can else stay
        if decision == 0:
            # Check blocking
            if not isBlocked(enemy.X, enemy.Y + ymove, True):
                enemy.move(enemy.X, enemy.Y + ymove)

            elif not isBlocked(enemy.X + xmove, enemy.Y, True):
                enemy.move(enemy.X + xmove, enemy.Y)

        else:
            if not isBlocked(enemy.X + xmove, enemy.Y, True):
                enemy.move(enemy.X + xmove, enemy.Y)

            elif not isBlocked(enemy.X, enemy.Y + ymove, True):
                enemy.move(enemy.X, enemy.Y + ymove)


#############################################
# Initialization & Main Loop
#############################################
def main(userID):
    global changeLevel

    global PlayerID
    PlayerID = userID

    global player

    PlayerName = sqlcon.sqlQuery("SELECT Name FROM User WHERE ID=%s" % PlayerID)[0][0]
    # playerstats all the values ID(Primary Key) and User_ID(Fotrign Key) are useless for now
    ID, MaxHP, CurrentHP, PositionX, PositionY, Attack, Defence, User_ID = sqlcon.getPlayersStats(PlayerID)[0]
    player = Actors.Player(PlayerName, MaxHP, CurrentHP, Attack, Defence, 0, PositionY, PositionX, '@')

    global exity, exitx

    global playerScore
    playerScore = getScore(PlayerID)[0][0]
    if playerScore == None:
        playerScore = 0

    global smap
    smap = []
    smap = sqlcon.getMapDataForID(PlayerID)

    global LevelID
    LevelID = sqlcon.getLevelIDforUserID(PlayerID)[0][0]
    changeLevel(LevelID)

    libtcod.console_set_default_foreground(0, libtcod.lighter_grey)
    for Object in objects:
        Object.draw()

    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, 1, 23, "           ")
        libtcod.console_print(0, 1, 23, "HP: %s/%s" % (player.Hp, player.HPMax))

        if player.Hp <= 0:
            gameOver()
            break

        libtcod.console_print(0, exitx, exity, ">")

        player.draw()

        libtcod.console_flush()  # draws(flushes) the buffer

        player.clear()

        for Enemy in enemies:
            Enemy.clear()

        # handle keys and exit game if needed
        exit = handleKeys()

        if levelChange:
            continue

        moveEnemies()

        libtcod.console_set_default_foreground(0, libtcod.green)
        for Enemy in enemies:
            Enemy.draw()


        if exit:
            break
    sqlcon.endConnection()


if __name__ == '__main__':
    print "Don't run this one run RunGame.py instead"
    sqlcon.endConnection()
