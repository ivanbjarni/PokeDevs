





class InvCard(object):
	name		= ""		#String		Name of inventory card
	health		= 0			#int 		Healing power of card
	stamina		= 0			#int 		Stamina boost from card
	stun		= False		#boolean	If true you are not stunned anymore 		
	damageBoost	= 0			#double		Tells you how much damage boost in %	
	defenseBoost= 0 		#double 	Tells you how much defense boost is in % (less than 1 is good)
	weakExploit = 0			#double 	Increases the damage multiplier when attacking someone who has weakness against you by this amount
	hitBoost	= 0			#double		Permanently increases the pokemon's chance to hit (reduces the chance to miss)
	critBoost 	= 0 		#double		Permanently increases the pokemon's chance to crit
	bitmap      = None 		#bitmap     Image to represent card

	def __init__(self, name, health, stamina, stun, damageBoost, defenseBoost, weakExploit, hitBoost, critBoost):
		self.name = name
		self.health = health
		self.stamina = stamina
		self.stun = stun
		self.damageBoost = damageBoost
		self.defenseBoost = defenseBoost
		self.weakExploit = weakExploit
		self.hitBoost = hitBoost
		self.critBoost = critBoost

	def getName(self):
		return self.name
	def getInfo(self):
		info = ""
		#info += " "+self.name+"\n "
		if(self.health != 0):
			info += "HP boost: "+str(self.health)+"\n "
		if(self.stamina != 0):
			info += "Sta. boost: "+str(self.stamina)+"\n "
		if(self.stun):
			info += "Stun off"+"\n "
		if(self.damageBoost != 0.0):
			info += "Dam. boost: "+str(self.damageBoost*100-100)+"%\n "
		if(self.defenseBoost != 0.0):
			info += "Def. boost: "+str(self.defenseBoost*100-100)+"%\n "
		if(self.weakExploit != 0.0):
			info += "SE. boost: "+str(self.weakExploit)+"\n "
		if(self.hitBoost != 0.0):
			info += "Hit boost: "+str(self.hitBoost)+"\n "
		if(self.critBoost != 0.0):
			info += "Crit boost: "+str(self.critBoost)
		return info

	def __str__(self):
		return self.name

	