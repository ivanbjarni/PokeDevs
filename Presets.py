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
		0	: Attack("Empty", 0, 0, 0, 0, "normal"),				# Empty Attack
		22	: Attack("VineWhip", 7, 10, 0, 0, "grass"),				# VineWhip
		33	: Attack("Tackle", 7, 10, 0, 0, "normal"),				# Tackle
		44	: Attack("Bite", 15, 20, 0, 0, "normal"),				# Bite
		45	: Attack("Growl", 5, 5, 0, 0, "normal"),				# Growl
		52	: Attack("Ember", 10, 10, 0, 0, "fire"),				# Ember
		53	: Attack("Flamethrower", 18, 30, 0, 0, "fire"),			# Flamethrower
		55	: Attack("WaterGun", 18, 30, 0, 0, "water"),			# WaterGun
		61	: Attack("BubbleBeam", 28, 34, 0, 0, "water"),			# BubbleBeam
		75	: Attack("RazorLeaf", 18, 30, 0, 0, "grass"),			# RazorLeaf
		76	: Attack("SolarBeam", 34, 80, 0, 0, "grass"),			# SolarBeam
		98	: Attack("QuickAttack", 12, 20, 0, 0, "normal"),		# QuickAttack
		116 : Attack("Withdraw",0,-17,-5,0,"water"),				# Withdraw
		116 : Attack("FocusEnergy",0,-25,0,0,"normal"),				# FocusEnergy
		424 : Attack("FireFang", 10, 12, 0, 2, "fire"),				# FireFang
		486	: Attack("Thunder", 30, 50, 10, 0, "electric"),			# Thunder
		517	: Attack("Inferno", 25, 50, 0, 0, "fire"),				# Inferno
		678	: Attack("ElectroBall", 18, 30, 0, 0, "electric")		# ElectroBall
		}

	def initCards(self):
		self.cards = {
		1	: Card("Bulbasaur", 39, 90, [self.ga("Tackle"), self.ga("RazorLeaf"), self.ga("VineWhip"), self.ga("SolarBeam")], "grass", "fire", "water"),
		4	: Card("Charmander", 39, 90, [self.ga("Tackle"), self.ga("Growl"), self.ga("Flamethrower"), self.ga("Ember")], "fire", "water", "grass"),
		7	: Card("Squirtle", 39, 90, [self.ga("Tackle"), self.ga("BubbleBeam"), self.ga("Withdraw"), self.ga("WaterGun")], "water", "grass", "fire"),
		25	: Card("Pikachu", 35, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("ElectroBall"), self.ga("Thunder")], "electric", "ground", "electric"),
		133	: Card("Eevee", 40, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("FocusEnergy"), self.ga("Bite")], "normal", "ground", "psychic")
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
		print "Attack not found: getAttackByName"
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