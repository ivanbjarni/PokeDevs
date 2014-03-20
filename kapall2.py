from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *
from util import *
from Presets import *
from Main import *
from Gui import *

#-------------------
# Attempt to hook the Gui up to the Gameplay
#-------------------

if __name__=="__main__":
	#Load attacks and cards
	presets = Presets()

	p1 = Player("player1")
	p1.hand = Hand()
	p1.deck = Deck()
	for i in xrange(0,6):
		p1.deck.add(presets.getRandomCard())
	p1.mainCard = presets.getRandomCard()

	#create player 1 give him a hand, random mainCard and a random 10card deck
	p2 = Player("player2")
	p2.hand = Hand()
	p2.deck = Deck()
	for i in xrange(0,6):
		p2.deck.add(presets.getRandomCard())
	p2.mainCard = presets.getRandomCard()

#	for i in p1.deck.cards:
#		print i.name
#
#	print '===='
#
#	for i in p2.deck.cards:
#		print i.name
	
	game = Main([p1, p2])
	app = wx.App()
	gui = MainFrame()
	gui.gamePanel.setupPanel(p1, p2)
	gui.Show()
	app.MainLoop()