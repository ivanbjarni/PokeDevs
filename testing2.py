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
p1.deck = Deck()
for i in xrange(0,10):
	p1.deck.add(presets.getRandomCard())
p1.mainCard = presets.getRandomCard()
p2 = Player("p2")
p2.hand = Hand()
p2.deck = Deck()
for i in xrange(0,10):
	p2.deck.add(presets.getRandomCard())
p2.mainCard = presets.getRandomCard()

game = Main([p1,p2])
game.gameLoop()
