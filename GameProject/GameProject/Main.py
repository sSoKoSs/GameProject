import libtcodpy as libtcod
import Actors

##################################### INIT #####################################
# actual size of the window
SCREEN_WIDTH = 25
SCREEN_HEIGHT = 25

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'ConsoleGame', False)
##################################### INIT #####################################



player = Actors.Player(Name=" ", HPMax=10, Hp=10, Attack=3, Defence=1, Coins=0, Y=12, X=12, Symbol='@')

objects = []



# ########################TESTMAP#########################x25 y22 550 chars
smap = ['#########################',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#                       #',
        '#########################']
#########################################################


# def Name():
#     global playerName
#
#     libtcod.console_clear(0)
#     libtcod.console_print(0, 0, 0, "What is your name")
#     libtcod.console_print(0, 0, 1, playerName)
#     libtcod.console_print(0, 0, 2, "Press the Enter key to continue")
#     libtcod.console_flush()
#     key = libtcod.console_wait_for_keypress(False)
#
#     while not key.vk == libtcod.KEY_ENTER:
#         playerName += str(unichr(key.vk))
#
#         libtcod.console_print(0, 0, 0, "What is your name")
#         libtcod.console_print(0, 0, 1, playerName)
#         libtcod.console_print(0, 0, 2, "Press the Enter key to continue")
#         libtcod.console_flush()
#         key = libtcod.console_wait_for_keypress(False)
#
#     return playerName


def handleKeys():
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

    if isBlocked(playerx, playery):
        pass # TODO target if enemy
    else:
        player.move(playerx, playery)


def makeMapObjects(first):
    global smap

    if first:
        libtcod.console_clear(0)
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, 1, 24, "<v>^ : move around")

        for y in range(SCREEN_HEIGHT-3):
            for x in range(SCREEN_WIDTH):
                if smap[y][x] == '#':
                    objects.append(Actors.Wall(Y=y, X=x, Symbol='#', Blocks=True))
                #TODO make Grunts here too
                #libtcod.console_put_char(0, x, y, smap[y][x], libtcod.BKGND_NONE)


def isBlocked(x, y):
    # check for any blocking objects
    for Object in objects:
        if Object.Blocks and Object.X == x and Object.Y == y:
            return True

    return False


#############################################
# Initialization & Main Loop
#############################################
def main():
    # login()
    makeMapObjects(True)
    for Object in objects:
        Object.draw()

    while not libtcod.console_is_window_closed():
        player.draw()
        #print player.Y, " ", player.X
        libtcod.console_flush()  # draws(flushes) the buffer

        player.clear()

        # handle keys and exit game if needed
        exit = handleKeys()
        if exit:
            break


if __name__ == '__main__':
    main()
