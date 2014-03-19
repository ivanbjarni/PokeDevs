from Attack import *
import random
from constants import *




class Card(object):
	name 		= ""		#String		Name of pokemon
	health 		= 100		#int 		Current health
	healthMax 	= 100		#int 		Maximum health
	stamina 	= 100		#int 		Current stamina used for attacks
	staminaMax 	= 100		#int 		Maximum stamina used for attacks
	attacks 	= []		#Attack[] 	List of attacks the pokemon/card has
	poketype 	= "normal" 	#String		Type the pokemon has, all lowercase ("normal", "fire", "water","psychic", "grass", "electric", "ground" ) 
	weakness 	= "normal" 	#String		Type the pokemon is weak against, same format as above
	resistance 	= "normal"	#String		Type the pokemon is strong against, same format as above
	stun 		= 0			#int 		Turns that pokemon will be stunned
	bitmap		= None		#Bitmap		Image that represents the card on the playing mat

	def __init__(self, name, health,  stamina, attacks, poketype, weakness, resistance):
		self.name = name
		self.health = health
		self.healthMax = health
		self.stamina = stamina
		self.staminaMax = stamina
		self.attacks = attacks
		self.poketype = poketype 
		self.weakness =  weakness
		self.resistance = resistance
			
	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is Attack
	# After: b is true if card dies, false otherwise
	def __str__(self):
		return self.name

	def getAttacks(self):
		s=""
		for a in self.attacks:
			s += " - "
			s += str(a) + "\n"
		return s

	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is Attack
	# After: b is true if attack succeeds, false otherwise.
	#		 Also prints out on console what happens.
	def attack(self, atk, card):
		if(atk.name == "Metronome"):
			atk.staminaCost = round(random.random()*metronomeAmount+metronomeBase)
			atk.damage 		= round(random.random()*metronomeAmount+metronomeBase)
			atk.healthCost 	= round(random.random()*metronomeAmount+metronomeBase)
		if(self.stamina < atk.staminaCost):
			print "Not Enough Stamina"
			return False
		if(self.isDead()):
			print "Uh-oh you are trying to attack with a dead pokemon"
			return False
		if(self.isStunned()):
			print str(self)+" tried to use "+str(atk)+" but he is stunned."
			return True

		self.stamina -= atk.staminaCost
		self.health  -= atk.healthCost
		self.health   = min(self.health , self.healthMax)
		self.stamina = min(self.stamina, self.staminaMax)

		message = ""

		damage = atk.damage
		#resistance
		if self.poketype == card.resistance and damage !=0:
			damage *= resistanceMultiplier
			message = ". It's not very effective!"
		#weakness
		if atk.poketype == card.weakness and damage !=0:
			damage *= weaknessMultiplier
			message = ". It's super effective!"
		#crit
		if random.random() < critChance and damage !=0:
			damage *= critMultiplier
			message = ", It's a critical hit!"
		#miss
		if random.random()<missChance and damage !=0:
			damage = 0
			message = ", but it missed!"
		
		if(atk.stun!=0 and random.random() < stunChance):
			card.stun = atk.stun
			message += "(Stun applied for "+str(atk.stun)+" turns)"

		print str(self)+" used "+str(atk)+message
		print "Damage done: "+str(damage)
		card.health  -= damage
		
		return True

	# Usage: b = c.isDead()
	# Before: Nothing
	# After: b is true if c is dead, false otherwise. 
	def isDead(self):
		return (self.health<=0)

	# Usage: b = c.isStunned()
	# Before: Nothing
	# After: b is true if c is stunned, false otherwise. 
	def isStunned(self):
		return (self.stun>0)

	# Usage: c.applyEffects()
	# Before: Nothing
	# After: applies effects that happen to card during turn 
	def applyEffects(self):
		if self.stun > 0:
			self.stun -= 1