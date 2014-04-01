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
from Gui import *
from AI import *

#-------------------
# Beginning to attempt to hook the Gui up to the Gameplay
#-------------------

if __name__=="__main__":
	#Load attacks and cards
	presets = Presets()

	#create player 1 give him a hand, random mainCard and a random 10card deck
	p1 = Player("player1")
	p1.hand = Hand()
	p1.inv = Inventory()
	p1.deck = presets.gd("random")
	p1.invdeck = InvDeck()
	p1.mainCard = p1.deck.cards[0]
	for i in xrange(0,100):
		p1.invdeck.add(presets.getRandomInvCard())

	#create player 1 give him a hand, random mainCard and a random 10card deck
	p2 = Player("computer")
	p2.hand = Hand()
	p2.inv = Inventory()
	p2.deck = Deck()
	p2.invdeck = InvDeck()
	for i in xrange(0,10):
		p2.deck.add(presets.getRandomCard())
	p2.mainCard = p2.deck.cards[0]
	for i in xrange(0,100):
		p2.invdeck.add(presets.getRandomInvCard())
	
	game = Main([p1, p2])
	app = wx.App()
	gui = MainFrame(game)
	gui.gamePanel.setupPanel(p1, p2)
	gui.Show()
	app.MainLoop()
#	gui = RunGuiThread()
#	gui.start()
#	print 'what'