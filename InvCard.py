





class InvCard(object):
	name		= ""		#String		Name of inventory card
	health		= 0			#int 		Healing power of card
	stamina		= 0			#int 		Stamina boost from card
	stun		= False		#boolean	If true you are not stunned anymore 		
	damageBoost	= 0			#double		Tells you how much damage boost in %
	bitmap      = None 		#bitmap     Image to represent card

	def __init__(self, name, health, stamina, stun, damageBoost):
		self.name = name
		self.health = health
		self.stamina = stamina
		self.stun = stun
		self.damageBoost = damageBoost

	def __str__(self):
		return self.name

	