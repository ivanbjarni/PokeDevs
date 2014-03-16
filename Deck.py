from Card import *
import random




class Deck(object):
	cards 		= []		#Card[]		List of cards in the deck

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

	# Usage: card = deck.draw()
	# Before: deck not empty
	# After: card is the top card of the deck which has been removed
	def draw(self):
		return self.cards.pop()

	# Usage: card = deck.remove()
	# Before: index is a valid index in deck.cards
	# After: card is the card with the given index which has been removed from the deck
	def remove(self, index):
		return self.cards.pop(index)

	# Usage: deck.add(card)
	# Before: Nothing 
	# After: Card has been added to the deck
	def add(self, card):
		self.cards.append(card)

	# Usage: i=deck.getIndexOf(name)
	# Before: Nothing
	# After: i is the index of name if name is not in the deck then i=-1
	def getIndexOf(self,name):
		for i in range(0,len(self.cards)):
			if(self.cards[i].name == name):
				return i
		return -1

	# Usage: bool=deck.isEmpty()
	# Before: Nothing
	# After: bool is true if deck is empty else false
	def isEmpty(self):
		return not self.cards
