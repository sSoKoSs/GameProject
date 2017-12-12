# GameProject
Console game that will query to a DataBase and load the data to client's game.

# Requirements
Python 2.7

libtcodpy

# How to make a level:
##### Levels are constructed with symbols like(see exampleLevels to get a better sense of it)
- @ = players starting position (use this only when you want the player to not start at the last stair OR when its the first level)
- \# = Wall
- ' ' = (this is a space character don't put these ' ) = free space everything can move there
- G = Grunt/Goblin (moves to the player in a semi random movement, not diagonally and no pathfinding)
- $ = coins (they give score points)
- & = health
- A = Attack
- D = Defence

### IMPORTANT:
The level **HAS** to be 25 (x axis) * 22 (y axis) (550) characters long **WITHOUT** newlines (meaning one line)
if you put a character that is not known it will be ignored(but it will be counted thats why no newlines) and
a space(' ') will be placed instead.

After you make one insert/update it into the database in Level.data
