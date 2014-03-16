from Deck import *
from Hand import *
from Card import *
from util import *


class Presets(object):
	decks		= []		#Decks		Predefined cecks of cards to be used
	cards		= []		#Cards		Predefined cards to be used
	attacks 	= []		#Attacks 	Predefined attacks to be used

	def __init__(self):
		self.initAttacks()
		self.initCards()

	def __str__(self):
		return "presets"

	def initAttacks(self):
		self.attacks ={
		0	: Attack("Empty", 0, 0, 0, 0, "normal"),				
		10	: Attack("Scratch", 10, 10, 0, 0, "normal"),			
		22	: Attack("VineWhip", 7, 10, 0, 0, "grass"),				
		33	: Attack("Tackle", 7, 10, 0, 0, "normal"),				
		36	: Attack("TakeDown", 10, 15, 0, 0, "normal"),			
		38	: Attack("DoubleEdge", 17, 22, 0, 0, "normal"),			
		44	: Attack("Bite", 15, 20, 0, 0, "normal"),				
		45	: Attack("Growl", 5, 5, 0, 0, "normal"),				
		52	: Attack("Ember", 10, 10, 0, 0, "fire"),			
		53	: Attack("Flamethrower", 26, 30, 0, 0, "fire"),			
		55	: Attack("WaterGun", 18, 30, 0, 0, "water"),			
		56	: Attack("HydroPump", 50, 75, 0, 0, "water"),			
		61	: Attack("BubbleBeam", 28, 35, 0, 0, "water"),			
		75	: Attack("RazorLeaf", 18, 30, 0, 0, "grass"),			
		76	: Attack("SolarBeam", 34, 80, 0, 0, "grass"),			
		80	: Attack("PetalDance", 15, 30, 0, 0, "grass"),			
		83	: Attack("FireSpin", 28, 30, 0, 0, "fire"),				
		98	: Attack("QuickAttack", 12, 20, 0, 0, "normal"),	
		110 : Attack("Withdraw",0, -17, -5, 0, "normal"),			
		116 : Attack("FocusEnergy", 0, -25, 0, 0, "normal"),	
		145 : Attack("Bubble", 10, 10, 0, 0, "water"),	
		229 : Attack("RapidSpin", 7, 23, 0, 2,"normal"),			
		352 : Attack("WaterPulse", 30, 30, 0, 0,"water"),			
		394 : Attack("FlareBlitz", 40, 50 ,0,0,"fire"),				
		424 : Attack("FireFang", 15, 12, 0, 2, "fire"),				
		486	: Attack("Thunder", 30, 50, 10, 0, "electric"),			
		517	: Attack("Inferno", 25, 50, 0, 0, "fire"),				
		572	: Attack("PetalBlizzard", 35, 60, 0, 0, "grass"),
		678	: Attack("ElectroBall", 18, 30, 0, 0, "electric")
		}

	def initCards(self):
		self.cards = {
		1	: Card("Bulbasaur", 45, 90, [self.ga("Tackle"), self.ga("RazorLeaf"), self.ga("VineWhip"), self.ga("SolarBeam")], "grass", "fire", "water"),
		2   : Card("Ivysaur", 60, 80, [self.ga("TakeDown"), self.ga("RazorLeaf"), self.ga("DoubleEdge"), self.ga("SolarBeam")], "grass", "fire", "water"),
		3   : Card("Venusaur", 80, 82, [self.ga("VineWhip"), self.ga("PetalDance"), self.ga("SolarBeam"), self.ga("PetalBlizzard")], "grass", "fire", "water"),
		4	: Card("Charmander", 39, 100, [self.ga("Tackle"), self.ga("Growl"), self.ga("Flamethrower"), self.ga("Ember")], "fire", "water", "grass"),
		5	: Card("Charmeleon", 58, 90, [self.ga("Scratch"), self.ga("FireFang"), self.ga("Flamethrower"), self.ga("FireSpin")], "fire", "water", "grass"),
		6	: Card("Charizard", 78, 85, [self.ga("Ember"), self.ga("FireFang"), self.ga("Inferno"), self.ga("FlareBlitz")], "fire", "water", "grass"),
		7	: Card("Squirtle", 44, 90, [self.ga("Tackle"), self.ga("BubbleBeam"), self.ga("Withdraw"), self.ga("WaterGun")], "water", "grass", "fire"),
		8	: Card("Wartotle", 59, 100, [self.ga("Tackle"), self.ga("RapidSpin"), self.ga("Withdraw"), self.ga("WaterPulse")], "water", "electric", "fire"),
		9	: Card("Blastoise", 79, 105, [self.ga("Bubble"), self.ga("WaterPulse"), self.ga("WaterGun"), self.ga("HydroPump")], "water", "electric", "fire"),
		10	: Card("Caterpie", 45, 100, [self.ga("Tackle"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Empty")], "grass", "electric", "grass"),
		25	: Card("Pikachu", 35, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("ElectroBall"), self.ga("Thunder")], "electric", "ground", "electric"),
		133	: Card("Eevee", 55, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("FocusEnergy"), self.ga("Bite")], "normal", "ground", "psychic")
		



		}

	#Short for get attack
	def ga(self, attack):
		if isNumber(attack):
			return self.attacks[attack]
		else:
			return self.getAttackByName(attack)

	def getAttackByName(self, string):
		for key, val in self.attacks.iteritems():
			if val.name == string:
				return val
		print "Attack not found: getAttackByName. attack: "+string
		return -1


	#Short for get Card
	def gc(self, card):
		if isNumber(card):
			return self.cards[card]
		else:
			return self.getCardByName(card)

	def getCardByName(self, string):
		for key, val in self.cards.iteritems():
			if val.name == string:
				return val
		print "card not found: getCardByName"
		return -1