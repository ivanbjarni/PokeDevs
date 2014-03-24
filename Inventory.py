from InvCard import *
from constants import *




class Inventory(object):
	invCards 		= []		#Card[]		List of invCards in the hand

	def __init__(self):
		self.invCards = []

	def __str__(self):
		s = ""
		for c in self.invCards:
			s +=  str(c) + ", "
		return s

	# Usage: card = hand.remove()
	# Before: hand not empty
	# After: card is the card with the given index which has been removed from the hand
	def remove(self, index):
		return self.invCards.pop(index)

	# Usage: hand.add(card)
	# Before: Nothing
	# After: Card has been added to the hand
	def add(self, card):
		self.invCards.append(card)

	# Usage: i=hand.getIndexOf(name)
	# Before: Nothing
	# After: i is the index of name if name is not in the hand then i=-1
	def getIndexOf(self,name):
		for i in range(0,len(self.invCards)):
			if(self.invCards[i].name == name):
				return i
		return -1

	def isFull(self):
		return len(self.invCards)>= invCardsMax