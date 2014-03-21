from Card import *






class Hand(object):
	cards 		= []		#Card[]		List of cards in the hand
	cardsMax	= 6			#int 		Maximum amount of cards a player can hold	

	def __init__(self):
		self.cards = []

	def __str__(self):
		s = ""
		for c in self.cards:
			s +=  str(c) + ", "
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
			if(self.cards[i].name == name):
				return i
		return -1

	# Usage: b=h.isFull()
	# Before: Nothing
	# After: returns true if hand you can't have more cards in your hand
	def isFull(self):
		return len(self.cards)>= self.cardsMax

	# Usage: i=h.getNameOfType(type)
	# Before: type is string
	# After: i is the name of a card with type type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfType(self, poketype):
		for a in self.cards:
			if a.poketype in poketype:
				return str(a)
		return "none"

	# Usage: i=h.getNameOfNotWeakness(type)
	# Before: type is string
	# After: i is the name of a card not with weakness type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfNotWeakness(self, poketype):
		for a in self.cards:
			if a.weakness not in poketype:
				return str(a)
		return "none"

	# Usage: i=h.getNameOfType(type)
	# Before: type is string
	# After: i is the name of a card with resistance type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfResistance(self, poketype):
		for a in self.cards:
			if a.resistance in poketype:
				return str(a)
		return "none"