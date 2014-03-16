from Card import *



class Hand(object):
	cards 		= [];		#Card[]		List of cards in the hand

	def __init__(self):
		self.cards = []

	def __str__(self):
		s = ""
		for c in cards:
			s = s + c
		return s


	