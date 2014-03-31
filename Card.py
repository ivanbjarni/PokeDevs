from Attack import *
import random
from constants import *
import copy
from util import *


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
	turnsOut	= 0			#int 		How many turns a pokemon has been on the field
	turnsStunned= 0 		#int 		How many turns a pokemon has been stunned

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
			s += "- "
			s += str(a) + "\n"
		return s

	# Usage: b = c.attack(atk, card)
	# Before: card is Card and atk is Attack
	# After: b is true if attack succeeds, false otherwise.
	#		 Also prints out on console what happens.
	def attack(self, atk, card, textLog):
		if(atk.name == "Metronome"):
			atk.staminaCost = round(random.random()*metronomeAmount+metronomeBase)
			atk.damage 		= round(random.random()*metronomeAmount+metronomeBase)
			atk.healthCost 	= round(random.random()*metronomeAmount+metronomeBase)
		if(atk.name == "Transform"):
			scard = self.transformTo(card)
			print "ditto transformed to "+scard
			textLog.append("ditto transformed to "+scard+"\n")
			return True
		if(self.stamina < atk.staminaCost):
			print "Not Enough Stamina "
			textLog.append("Not Enough Stamina\n")
			return False
		if(self.isDead()):
			print "Uh-oh you are trying to attack with a dead pokemon"
			textLog.append("Uh-oh you are trying to attack with a dead pokemon\n")
			return False
			return False
		if(self.isStunned() and random.random() > stunSuccessRate):
			print str(self)+" tried to use "+str(atk)+" but he is stunned."
			textLog.append(str(self)+" tried to use "+str(atk)+" but he is stunned.\n")
			return True

		oldhp = self.health
		oldsta= self.stamina
		self.stamina -= atk.staminaCost
		self.health  -= atk.healthCost
		self.health   = min(self.health , self.healthMax)
		card.health   = min(card.health , card.healthMax)
		self.stamina = min(self.stamina, self.staminaMax)
		stun = atk.stun

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
			#make heal and stamina recovery fail as well as stun and dmg:
			self.stamina= min(self.stamina,oldsta)
			self.health = min(self.health ,oldhp)
			stun = 0;
		
		realStunChance = max(stunChance - (card.turnsStunned/turnsToMinStun)*(stunChance-stunChanceMin),stunChanceMin)
		if(stun!=0 and random.random() < realStunChance):
			card.setStun(atk.stun)
			message += "(Stun applied for "+str(stun)+" turns)"
		elif stun!=0:
			message += "(Stun not applied.)"

		print str(self)+" used "+str(atk)+message
		print "Damage done: "+str(damage)
		textLog.append(str(self)+" used "+str(atk)+message)
		textLog.append("Damage done: "+str(damage)+"\n")
		card.health  -= damage

		if(card.isDead() and isLogged):
			pokemonCounterLog(self.name,"pokemonKillers.txt")
			pokemonCounterLog(card.name,"pokemonVictims.txt")

		return True


	# Usage: b = c.use(card)
	# Before: card is inventorycard and user is pokemoncard
	# After: b is true if useage succeeds, false otherwise.
	#		 Also prints out on console what happens.
	def use(self, card, textLog):
		if card.stamina > 0:
			self.stamina += card.stamina
			print str(self)+ "'s stamina increased by "+str(card.stamina)
			textLog.append(str(self)+ "'s stamina increased by "+str(card.stamina)+"\n")
		if card.health > 0:
			self.health  += card.health
			print str(self)+"'s health increased by "+str(card.health)
			textLog.append(str(self)+ "'s health increased by "+str(card.health)+"\n")
		self.health   = min(self.health , self.healthMax)
		self.stamina = min(self.stamina, self.staminaMax)
		if card.stun:
			self.stun = 0
			print str(self)+" is not stunned anymore"
			textLog.append(str(self)+" is not stunned anymore\n")
		if card.damageBoost > 1:
			self.setDamageMultiplier(card.damageBoost)
			print "Damage boost!"
			textLog.append(str(self)+" got  a damage boost!\n")
		if card.defenseBoost < 1:
			self.setDefenseMultiplier(card.defenseBoost)
			print "Defense boost!"
			textLog.append(str(self)+" got a defense boost!\n")
		if card.hitBoost > 0:
			self.hitDiff += card.hitBoost
			print "Hit Boost"
			textLog.append(str(self)+" got a hit boost!\n")
		if card.critBoost > 0:
			self.critDiff += card.critBoost
			print "Crit Boost"
			textLog.append(str(self)+" got a crit boost!\n")
		if card.weakExploit != 0:
			self.weakExploit = card.weakExploit
			print "Super effective moves boosted"
			textLog.append(str(self)+" boosted super effective moves!\n")

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

	def getInfo(self):
		res = ''
		res += 'HP: '+str(self.health)+'/'+str(self.healthMax)+'\n'
		res += 'Stamina: '
		res += str(self.stamina) + '/'+ str(self.staminaMax)
		res += '\nAttacks: \n'
		res += self.getAttacks()
		res += 'Type: '+str(self.poketype).title()+'\n'
		res += 'Wkn: '+str(self.weakness).title()+'\n'
		res += 'Res: '+str(self.resistance).title()+'\n'
		return res

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
			if self.attacks[x].staminaCost <= self.stamina:
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
				for x in range(0, len(nonattackdamagelist)):
					picked = nonattackdamagelist[x]
					if self.health < self.healthMax * 0.85 and self.attacks[picked].healthCost < 0:
						return picked
					elif self.stamina < self.staminaMax * 0.85 and self.attacks[picked].staminaCost < 0:
						return picked
					elif self.attacks[picked].stun > 0:
						return picked
				return nonattackdamagelist[0]		
		else:
			return 0

	# Usage: c.setStun(turns)
	# Before: Nothing
	# After: c is stunned for stun turns
	def setStun(self,turns):
		self.stun = turns
		self.turnsStunned += turns

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
		ratio = float(self.health)/float(self.healthMax)
		self.health = card.healthMax * ratio
		self.healthMax = card.healthMax
		self.stamina = card.staminaMax
		self.staminaMax = card.staminaMax
		self.attacks = copy.deepcopy(card.attacks)
		return card.name
