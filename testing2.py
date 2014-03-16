from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *
from util import *
from Presets import *
from Main import *

presets = Presets()

p1 = Player("p1")
p1.mainCard = presets.gc("Charmander")
p2 = Player("p2")
p2.mainCard = presets.gc("Eevee")

game = Main([p1,p2])
game.gameLoop()
