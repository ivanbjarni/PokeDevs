from Deck import *
from Hand import *
from Card import *




class Player(object):
	name 		= ""		#String		Name of player
	deck		= None		#Deck		Deck of player
	invdeck		= None		#Deck 		Inventorydeck of player
	graveyard 	= None		#Deck 		Graveyard, where dead cards go
	hand		= None		#Hand 		Cards that player has in his hand
	mainCard	= None		#Card		Players main card on the field
	points		= 0			#int 		how many pokemon's in you have slain! (jk they don't die, they just faint.)
	tries		= []		#bool[]		A boolean  array that tells you which attacks you have tried to use

	def __init__(self, name):
		self.name = name
		self.graveyard = Deck()

	def __str__(self):
		return self.name

	# Usage: b = p.attack(atk, player)
	# Before: player is Player and atk is the index nr of attack on main card
	# After: b is true if attack succeeds, false otherwise
	def attack(self,  nr,  player):
		atk = self.mainCard.attacks[nr]
		return self.mainCard.attack(atk, player.mainCard)

	# Usage: b = p.isAI()
	# Before: Nothing
	# After: b is true if player is ai(name is "computer"), false otherwise
	def isAI(self):
		return (self.name == "computer")