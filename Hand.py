from Card import *





class Hand(object):
	cards 		= []		#Card[]		List of cards in the hand
	cardsMax	= 6			#int 		Maximum amount of cards a player can hold	

	def __init__(self):
		self.cards = []

	def __str__(self):
		s = ""
		for c in self.cards:
			s = s +", "+ str(c)
		return s

	# Usage: card = hand.remove()
	# Before: hand not empty
	# After: card is the card with the given index which has been removed from the hand
	def remove(self, index):
		return self.cards.pop(index)

	# Usage: hand.add(card)
	# Before: Nothing 
	# After: Card has been added to the hand
	def add(self, card):
		self.cards.append(card)

	# Usage: i=hand.getIndexOf(name)
	# Before: Nothing
	# After: i is the index of name if name is not in the hand then i=-1
	def getIndexOf(self,name):
		for i in range(0,len(self.cards)):
			if(self.cards[i] == name):
				return i
		return -1

	def isFull(self):
		return len(self.cards)>= self.cardsMax