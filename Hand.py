from Card import *
from constants import *





class Hand(object):
	cards 		= []		#Card[]		List of cards in the hand

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
		return len(self.cards)>= cardsMax

	# Usage: i=h.getNameOfType(type)
	# Before: type is string
	# After: i is the name of a card with type type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfType(self, poketype):
		pokemon = "none"
		for a in self.cards:
			if a.poketype == poketype and pokemon == "none":
				pokemon = str(a)
			elif a.poketype == poketype and pokemon != "none":
				i = self.getIndexOf(str(pokemon))
				if self.cards[i].health + self.cards[i].stamina < a.health + a.stamina:
					pokemon = str(a)  	 
		return pokemon

	# Usage: i=h.getNameOfNotWeakness(type)
	# Before: type is string
	# After: i is the name of a card not with weakness type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfNotWeakness(self, poketype):
		pokemon = "none"
		for a in self.cards:
			if a.weakness != poketype and pokemon == "none":
				pokemon = str(a)
			elif a.weakness != poketype and pokemon != "none":
				i = self.getIndexOf(str(pokemon))
				if self.cards[i].health + self.cards[i].stamina < a.health + a.stamina:
					pokemon = str(a)  	 
		return pokemon

	# Usage: i=h.getNameOfType(type)
	# Before: type is string
	# After: i is the name of a card with resistance type if it exists in hand
	#			"none" if that card doesn't exist
	def getNameOfResistance(self, poketype):
		pokemon = "none"
		for a in self.cards:
			if a.resistance == poketype and pokemon == "none":
				pokemon = str(a)
			elif a.resistance == poketype and pokemon != "none":
				i = self.getIndexOf(str(pokemon))
				if self.cards[i].health + self.cards[i].stamina < a.health + a.stamina:
					pokemon = str(a)  	 
		return pokemon

	# Usage: a = b.findTheStrongest(self)
	# Before: Nothing
	# After: Returns the name of the strongest pokemon in hand
	def findTheStrongest(self):
		pokemon = str(self.cards[0])
		hpandstamina = self.cards[0].health + self.cards[0].stamina
		for x in self.cards:
			if(x.health + x.stamina > hpandstamina):
				pokemon = str(x)
				hpandstamina = x.health + x.stamina

		return pokemon

	# Usage: i=h.getNameOfHighestStats()
	# Before: nothing
	# After: i is the name of the card with the highest hp and stamina combined
	def getNameOfHighestStats(self):
		hpst = 0
		res = "none"
		for a in self.cards:
			if a.stamina+a.health>=hpst:
				hpst = a.stamina+a.health
				res = a.name
		return res