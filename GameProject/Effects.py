import libtcodpy as libtcod
import time


class text(object):
    def __init__(self, x, y, text):
        super(text, self).__init__()
        # the width and height are the same as the map cause we don't want to draw outside of the map
        self.textScreen = libtcod.console_new(25, 22)
        self.x = x
        self.y = y
        self.text = text

    def draw(self):
        libtcod.console_print(self.textScreen, self.x, self.y, self.text)
        libtcod.console_blit(self.textScreen, self.x, self.y, len(self.text), 1, 0, 0, 0, 1, 1)

    def clear(self):
        libtcod.console_print(self.textScreen, " " * len(self.text))
        libtcod.console_blit(self.textScreen, self.x, self.y, len(self.text), 1, 0, 0, 0, 1, 1)

    ####
    def play(self, length=1000):
        self.draw()
        time.sleep(length)
        self.clear()
