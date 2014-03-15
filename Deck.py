from Card import *
import random




class Deck(object):
	cards 		= [];		#Card[]		List of cards in the deck

	def __init__(self):
		self.cards = []

	def __str__(self):
		s = ""
		for c in self.cards:
			s = s + c
		return s

	# Usage: deck.shuffle()
	# Before: nothing
	# After: deck has been shuffled
	def shuffle(self):
		random.shuffle(self.cards)