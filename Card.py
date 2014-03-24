from Attack import *
import random
from constants import *
import copy



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
	dmgMulti	= 1 		#double		Damage multiplier 
	defMulti	= 1 		#double		Defense multiplier
	critDiff	= 0			#double		How much difference is between standard crit chance and the crit chance of this pokemon
	hitDiff		= 0			#double		How much difference is between standard hit chance and the hit chance of this pokemon
	weakExploit = 0			#double		How much additional % of damage you do with super effective moves

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
		if(atk.name == "Transform"):
			scard = self.transformTo(card)
			print "ditto transformed to "+scard
			return True
		if(self.stamina <= atk.staminaCost):
			print "Not Enough Stamina "
			return False
		if(self.isDead()):
			print "Uh-oh you are trying to attack with a dead pokemon"
			return False
		if(self.isStunned() and random.random() > stunSuccessRate):
			print str(self)+" tried to use "+str(atk)+" but he is stunned."
			return True

		oldhp = self.health
		oldsta= self.stamina
		self.stamina -= atk.staminaCost
		self.health  -= atk.healthCost
		self.health   = min(self.health , self.healthMax)
		card.health   = min(card.health , card.healthMax)
		self.stamina = min(self.stamina, self.staminaMax)

		message = ""
		
		damage = atk.damage * self.dmgMulti * card.defMulti
		#resistance
		if atk.poketype == card.resistance and damage >0:
			damage *= resistanceMultiplier
			message = ". It's not very effective!"
		#weakness
		if atk.poketype == card.weakness and damage >0:
			damage *= (weaknessMultiplier + self.weakExploit)
			message = ". It's super effective!"
		#crit
		if random.random() < (critChance+self.critDiff) and damage >0:
			damage *= critMultiplier
			message = ", It's a critical hit!"
		#miss
		if random.random()<(missChance-self.hitDiff):
			#we print different message depending on whether it is an actual attack
			if damage >0:
				message = ", but it missed!"
				damage = 0
			else:
				message = ", but it failed!"
			#make heal and stamina recovery fail as well:
			self.stamina= min(self.stamina,oldsta)
			self.health = min(self.health ,oldhp)
		
		if(atk.stun!=0 and random.random() < stunChance):
			card.stun = atk.stun
			message += "(Stun applied for "+str(atk.stun)+" turns)"
		elif atk.stun!=0:
			message += "(Stun not applied.)"

		print str(self)+" used "+str(atk)+message
		print "Damage done: "+str(damage)
		card.health  -= damage

		return True


	# Usage: b = c.use(card)
	# Before: card is inventorycard and user is pokemoncard
	# After: b is true if useage succeeds, false otherwise.
	#		 Also prints out on console what happens.
	def use(self, card):
		if card.stamina > 0:
			self.stamina += card.stamina
			print str(self)+ "'s stamina increased by "+str(card.stamina)
		if card.health > 0:
			self.health  += card.health
			print str(self)+"'s health increased by "+str(card.health)
		self.health   = min(self.health , self.healthMax)
		self.stamina = min(self.stamina, self.staminaMax)
		if card.stun:
			self.stun = 0
			print str(self)+" is not stunned anymore"
		if card.damageBoost > 1:
			self.setDamageMultiplier(card.damageBoost)
			print "Damage boost!"
		if card.defenseBoost < 1:
			self.setDefenseMultiplier(card.defenseBoost)
			print "Defense boost!"
		if card.hitBoost > 0:
			self.hitDiff += card.hitBoost
			print "Hit Boost"
		if card.critBoost > 0:
			self.critDiff += card.critBoost
			print "Crit Boost"
		if card.weakExploit != 0:
			self.weakExploit = card.weakExploit
			print "Super effective moves boosted"

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
		self.stamina = min (self.stamina+staminaEachRound,self.staminaMax)
		self.dmgMulti = 1
		self.defMulti = min(1,self.defMulti+defEachTurn)
		self.weakExploit = 0

	# Usage: c.shortInfo()
	# Before: Nothing
	# After: returns a short info about the card as string
	def shortInfo(self):
		return self.name+" (hp:"+str(self.health)+"/"+str(self.healthMax)+" sta:"+str(self.stamina)+"/"+str(self.staminaMax)+")"

	# Usage: b = c.hasHeal()
	# Before: Nothing
	# After: Returns True if Pokemon can heal it self, else False	
	def hasHeal(self):
		for x in range(0,4):
			if self.attacks[x].healthCost < 0:
				return True
		
		return False

	# Usage: b = c.needsHeal()
	# Before: Nothing
	# After: Returns True if pokemon needs to heal it self, else False 
	def needsHeal(self):
		needs = self.health < needsHealMark*self.healthMax
		return needs

	# Usage: x = c.findHeal()
	# Before: The card has the ability to heal
	# After: Returns the number of the attack that heals
	def findHeal(self):
		for x in range(0,4):
			if self.attacks[x].healthCost < 0:
				return x

	# Usage: b = c.hasStun()
	# Before: Nothing
	# After: Returns True if Pokemon can stun his enemy, else False	
	def hasStun(self):
		for x in range(0,4):
			if self.attacks[x].stun > 0:
				return True
		
		return False

	# Usage: x = c.findStun()
	# Before: The card has the ability to stun
	# After: Returns the number of the attack that stuns with least stamina cost	
	def findStun(self):
		stacost = 1000 #Just some high number
		attacknum = 0
		for x in range(0,4):
			if self.attacks[x].stun > 0 and self.attacks[x].staminaCost < stacost:
				attacknum = x
				stacost = self.attacks[x].staminaCost

		return attacknum

	# Usage: x = c.findHighestDamg()
	# Before: Nothing
	# After: Returns the number of the attack that deals most damage			
	def findHighestDamg(self):
		dam = self.attacks[0].damage
		attackNum = 0
		for x in range(1,4):
			if self.attacks[x].damage > dam:
				dam =  self.attacks[x].damage
				attackNum = x

		return attackNum

	# Usage: x = c.findPossibleAttacks()
	# Before: Nothing
	# After: Returns a list with the numbers of possible attacks concerning stamina			
	def findPossibleAttacks(self):
		possibleAtt = []
		for x in range(0,4):
			if self.attacks[x].staminaCost < self.stamina:
				possibleAtt.append(x)

		return possibleAtt


	# Usage: x = c.findClosestAttack(eneHP)
	# Before: Nothing
	# After: Returns the attack that deals closest damage to enemy HP
	def findClosestAttack(self, eneHP):
		attacknumberlist = self.findPossibleAttacks()
		attackdamagelist = []
		nonattackdamagelist = []
		if len(attacknumberlist) > 0:
			for x in range(0,4):
				if x in attacknumberlist and self.attacks[x].damage != 0:
					attackdamagelist.append(self.attacks[x].damage)
				elif x in attacknumberlist and self.attacks[x].damage == 0:
					nonattackdamagelist.append(x)
			if len(attackdamagelist) > 0:
				bestDamage = min(attackdamagelist, key=lambda x:abs(x-eneHP))
				for x in range(0,4):
					if x in attacknumberlist and bestDamage == self.attacks[x].damage:
						return x
			else:
				return nonattackdamagelist[0]
		else:
			return 0



	# Usage: b = c.hasStamina()
	# Before: Nothing
	# After: Returns True if Pokemon can increase its stamina, else False
	def hasStaminaBoost(self):
		for x in range(0,4):
			if self.attacks[x].staminaCost < 0:
				return True
		
		return False

	# Usage: b = c.needsStamina()
	# Before: Nothing
	# After: Returns True if pokemon needs more staminga, else False 
	def needsStamina(self):
		needs = self.stamina < needsStaminaMark*self.staminaMax
		return needs

	# Usage: x = c.findStamina()
	# Before: The card has the ability to increase its stamina
	# After: Returns the number of the attack that increases Stamina
	def findStamina(self):
		for x in range(0,4):
			if self.attacks[x].staminaCost < 0:
				return x

	# Usage: x = CanKillEne()
	# Before: Nothing
	# After: Returns true if attack damage is high enough til kill enemy
	def canKillEne(self, attacknum, eneHP):
		return self.attacks[attacknum].damage > eneHP

	# Usage: c.setDamageMultiplier(d)
	# Before: d is float
	# After: the damage multiplier of the pokemon is d
	def setDamageMultiplier(self, dmg):
		self.dmgMulti = dmg

	# Usage: c.setDamageMultiplier(d)
	# Before: d is float
	# After: the defense multiplier of the pokemon is d
	def setDefenseMultiplier(self, d):
		self.defMulti = d-defEachTurn

	# Usage: string = c.transformTo(card)
	# Before: card is card
	# After: c has transformed to card but still retains his health percent
	def transformTo(self, card):
		ratio = self.health/self.healthMax
		self.health = card.healthMax * ratio
		self.healthMax = card.healthMax
		self.stamina = card.staminaMax
		self.staminaMax = card.staminaMax
		self.attacks = copy.deepcopy(card.attacks)
		return card.name
