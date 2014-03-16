





class Attack(object):
	name 		= ""		#String		Name of attack
	damage 		= 10		#int 		Amount of damage
	staminaCost = 10		#int 		Amount of stamina reduced (or increased if it's  less than zero)
	healthCost	= 10		#int 		Amount of health reduced (or increased if it's  less than zero)
	stun		= 0			#int 		Duration of stun inflicted on the enemy
	poketype 	= "normal" 	#String		The type of the attack is, all lowercase ("normal", "fire", "water","psychic", "grass", "electric", "ground" ) 


	def __init__(self, name, damage, staminaCost, healthCost, stun, poketype):
		self.name = name
		self.damage = damage
		self.staminaCost = staminaCost
		self.healthCost = healthCost
		self.stun = stun
		self.poketype = poketype

	def __str__(self):
		return self.name

	# Usage: s=atk.info()
	# Before: nothing
	# After: s is a string that describes the attack
	def info(self):
		s = ""
		s+= self.name +" is a "+self.poketype+" type move that does "+str(self.damage)+" damage. "
		if(self.healthCost<0):
			s+="It heals you for "+str(-self.healthCost)+" hp. "
		elif(self.healthCost>0):
			s+="It drains your own life for "+str(self.healthCost)+" hp. "

		if(self.staminaCost<0):
			s+="Using this move will recover "+str(-self.staminaCost)+" stamina. "
		elif(self.staminaCost>0):
			s+="This move uses "+str(self.staminaCost)+" stamina. "
		return s