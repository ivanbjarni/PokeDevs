from Attack import *




class Card(object):
	name 		= ""		#String		Name of pokemon
	health 		= 100		#int 		Current health
	healthMax 	= 100		#int 		Maximum health
	stamina 	= 100		#int 		Current stamina used for attacks
	attacks 	= []		#Attack[] 	List of attacks the pokemon/card has
	poketype 	= "normal" 	#String		Type the pokemon has, all lowercase ("normal", "fire", "water","psychic", "grass", "electric", "ground" ) 
	weakness 	= "normal" 	#String		Type the pokemon is weak against, same format as above
	resistance 	= "normal"	#String		Type the pokemon is strong against, same format as above

	def __init__(self, name, health, healthMax, stamina, attacks, poketype, weakness, resistance):
		self.name = name
		self.health = health
		self.healthMax = healthMax
		self.stamina = stamina
		self.attacks = attacks
		self.poketype = poketype 
		self.weakness =  weakness
		self.resistance = resistance
			
	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is Attack
	# After: b is true if card dies, false otherwise
	def __str__(self):
		return name

	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is Attack
	# After: b is true if card dies, false otherwise
	def attack(self, atk, card):
		if(self.stamina < atk.staminaCost or self.health < atk.healthCost):
			return False
		
		self.stamina -= staminaCost
		self.health  -= healthCost
		self.health   = max(self.health , self.healthMax)

		card.health  -= damage
		
		return True
