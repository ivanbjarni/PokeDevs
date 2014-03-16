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
p1.hand = Hand()
p1.mainCard = presets.gc("Bulbasaur")
p2 = Player("p2")
p2.hand = Hand()
p2.mainCard = presets.gc("Blastoise")

game = Main([p1,p2])
game.gameLoop()
