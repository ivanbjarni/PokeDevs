from Deck import *
from Hand import *
from Card import *



class Player(object):
	name 		= ""		#String		Name of player
	deck		= None		#Deck		Deck of player
	graveyard 	= None		#Deck 		Graveyard, where dead cards go
	Hand		= None		#Hand 		Cards that player has in his hand
	mainCard	= None		#Card		Players main card on the field

	def __init__(self, name):
		self.name = name
		self.graveyard = Deck()

	def __str__(self):
		return self.name

	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is index nr of attack on main card
	# After: b is true if attack succeeds, false otherwise
	def attack(self,  nr,  player):
		atk = self.mainCard.attacks[nr]
		return self.mainCard.attack(atk, player.mainCard)