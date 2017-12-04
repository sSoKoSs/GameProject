import libtcodpy as libtcod


class Actor(object):
    def __init__(self, Y, X, Symbol, Blocks=False):
        super(Actor, self).__init__()
        self.Y = Y
        self.X = X
        self.Symbol = Symbol
        self.Blocks = Blocks

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_put_char(0, self.X, self.Y, self.Symbol, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(0, self.X, self.Y, ' ', libtcod.BKGND_NONE)


class Grunt(Actor):
    def __init__(self, Hp, Attack, Defence, Loot, Y, X, Symbol, Blocks=True):
        super(Grunt, self).__init__(Y, X, Symbol, Blocks)
        self.Hp = Hp
        self.Attack = Attack
        self.Defence = Defence
        self.Loot = Loot
        self.Enemy = True

    def LoseHealth(self, amount):
        amount -= self.Defence

        if amount > 0:
            self.Hp -= amount

        if self.Hp <= 0:
            self.clear()
            self.Blocks = False
            return self.X, self.Y

    def move(self, x, y):
        self.X = x
        self.Y = y


class Wall(Actor):
    def __init__(self, Y, X, Symbol='#', Blocks=True):
        super(Wall, self).__init__(Y, X, Symbol, Blocks)


class Player(Actor):
    def __init__(self, Name, HPMax, Hp, Attack, Defence, Coins, Y, X, Symbol):
        super(Player, self).__init__(Y, X, Symbol)
        self.Name = Name
        self.HPMax = HPMax
        self.Hp = Hp
        self.Attack = Attack
        self.Defence = Defence
        self.Coins = Coins

    def move(self, x, y):
        self.X = x
        self.Y = y
