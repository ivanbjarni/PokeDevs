from Attack import *
from Card import *
from Deck import *
from Inventory import *
from InvDeck import *
from InvCard import *
from Hand import *
from Player import *
from util import *
from Presets import *
from Main import *

#Load attacks and cards
presets = Presets()

#create player 1 give him a hand, random mainCard and a random 10card deck
p1 = Player("player1")
p1.hand = Hand()
p1.inv = Inventory()
p1.deck = Deck()
p1.invdeck = InvDeck()
for i in xrange(0,10):
	p1.deck.add(presets.getRandomCard())
p1.mainCard = presets.getRandomCard()
for i in xrange(0,50):
	p1.invdeck.add(presets.getRandomInvCard())


#create player 1 give him a hand, random mainCard and a random 10card deck
p2 = Player("computer")
p2.hand = Hand()
p2.inv = Inventory()
p2.deck = Deck()
p2.invdeck = InvDeck()
for i in xrange(0,10):
	p2.deck.add(presets.getRandomCard())
p2.mainCard = presets.getRandomCard()
for i in xrange(0,50):
	p2.invdeck.add(presets.getRandomInvCard())


#Create and run game
game = Main([p1,p2])
game.gameLoop()
