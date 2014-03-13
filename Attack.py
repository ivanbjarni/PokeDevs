




class Card(object):
	name 		= ""		#String		Name of attack
	damage 		= 10		#int 		Amount of damage
	staminaCost = 10		#int 		Amount of stamina reduced (or increased if it's  less than zero)
	healthCost	= 10		#int 		Amount of health reduced (or increased if it's  less than zero)
	stun		= 0			#int 		Duration of stun inflicted on the enemy
	poketype 	= "normal" 	#String		The type of the attack is, all lowercase ("normal", "fire", "water","psychic", "grass", "electric", "ground" ) 


	def __init__(self, name, damage, staminaCost, healthCost, stun, poketype):
		name = name
		damage = damage
		staminaCost = staminaCost
		healthCost = healthCost
		stun = stun
		poketype = poketype

	def __str__(self):
		return name