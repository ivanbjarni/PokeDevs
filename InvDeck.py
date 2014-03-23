from InvCard import *
import random




class InvDeck(object):
	invCards 		= []		#Card[]		List of invCards in the deck

	def __init__(self):
		self.invCards = []

	def __str__(self):
		s = ""
		for c in self.invCards:
			s = s + c
		return s

	# Usage: deck.shuffle()
	# Before: int
	# After: deck has been shuffled
	def shuffle(self):
		random.shuffle(self.invCards)

	# Usage: card = deck.draw()
	# Before: deck not empty
	# After: card is the top card of the deck which has been removed
	def draw(self):
		return self.invCards.pop()

	# Usage: card = deck.remove()
	# Before: index is a valid index in deck.invCards
	# After: card is the card with the given index which has been removed from the deck
	def remove(self, index):
		return self.invCards.pop(index)

	# Usage: deck.add(card)
	# Before: Nothing 
	# After: Card has been added to the deck
	def add(self, card):
		self.invCards.append(card)

	# Usage: i=deck.getIndexOf(name)
	# Before: Nothing
	# After: i is the index of name if name is not in the deck then i=-1
	def getIndexOf(self,name):
		for i in range(0,len(self.invCards)):
			if(self.invCards[i].name == name):
				return i
		return -1

	# Usage: bool=deck.isEmpty()
	# Before: Nothing
	# After: bool is true if deck is empty else false
	def isEmpty(self):
		if not self.invCards:
			return True
		return False
