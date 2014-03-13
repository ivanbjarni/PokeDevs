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

	def __str__(self):
		return name