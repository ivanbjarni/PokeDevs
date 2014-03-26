def clefable(self, pYou, pEne):
		calcAttack = pYou.mainCard.findClosestAttack(pEne.mainCard.health)   
		for x in range(0,4):
			if pYou.mainCard.attacks[x].name == "Metronome" and pYou.mainCard.attacks[x].staminaCost < pYou.mainCard.stamina:
				calcAttack = x
		return pYou.attack(calcAttack, pEne, self.textLog)

def chooseInvCardAI(self, pYou, pEne):
		yourCard = pYou.mainCard
		hasUsed = False 
		while(not hasUsed):
			offset = 0
			for j in range(0,len(pYou.inv.invCards)):
				i = j - offset
				if (pYou.inv.invCards[i].stamina > 0) and pYou.mainCard.needsStamina():
					print "I need stamina"
					stamina = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if stamina != -1:
						self.textLog.append("Opponent uses an inventory card to recover stamina\n")
						card = pYou.inv.remove(stamina)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].health > 0 and pYou.mainCard.needsHeal():
					print "I need heal"
					heal = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if heal != -1:
						self.textLog.append("Opponent uses an inventory card to recover health\n")
						card = pYou.inv.remove(heal)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].stun and pYou.mainCard.isStunned():
					print "I need to get unstunned"
					stun = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if stun != -1:
						self.textLog.append("Opponent uses an inventory card to remove stun\n")						
						card = pYou.inv.remove(stun)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].damageBoost > 1 and not pYou.mainCard.isStunned():
					print "I want to deal more DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						self.textLog.append("Opponent uses an inventory card to deal more damage\n")						
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].defenseBoost > 0 and pYou.inv.invCards[i].defenseBoost < 1 and not pYou.mainCard.health < 15:
					print "I want to take less DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						self.textLog.append("Opponent uses an inventory card to take less damage\n")						
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].weakExploit > 0 and pEne.mainCard.weakness == pYou.mainCard.poketype:
					print "I want to exploit your WEAKNESS!!\n"
					weaknessExploit = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if weaknessExploit != -1:
						self.textLog.append("Opponent uses an inventory card to exploit your weakness\n")						
						card = pYou.inv.remove(weaknessExploit)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].hitBoost > 0 and pYou.mainCard.health > 60:
					print "I want to hit BETTER!!\n"
					hitBoost = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if hitBoost != -1:
						self.textLog.append("Opponent uses an inventory card to hit better\n")					
						card = pYou.inv.remove(hitBoost)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif pYou.inv.invCards[i].critBoost > 0 and pYou.mainCard.health > 60:
					print "I want to critically hit BETTER!!\n"
					critBoost = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if critBoost != -1:
						self.textLog.append("Opponent uses an inventory card to raise critical hits\n")						
						card = pYou.inv.remove(critBoost)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
			hasUsed = True


def chooseAttackAI(self, pYou, pEne):		
		AICard = pYou.mainCard
		hasAttacked = False
		if len(pYou.inv.invCards) > 0:
			print "I have inventory things!"
			self.chooseInvCardAI(pYou, pEne)	
		#AI can't attack if his pokemon is stunned
		if AICard.isStunned():
			print str(AICard.name)+" is stunned"
			self.textLog.append(str(AICard)+" is stunned\n")
			hasAttacked = True
		calcAttack = pYou.mainCard.findClosestAttack(pEne.mainCard.health) #Best attack choise for damage
		if pYou.mainCard.canKillEne(calcAttack, pEne.mainCard.health):
			hasAttacked = pYou.attack(calcAttack, pEne, self.textLog)
		else:
			while(not hasAttacked):	
				#AI checks if it needs to and can heal
				heal = pYou.mainCard.findHeal()
				stamina = pYou.mainCard.findStamina()
				stun = pYou.mainCard.findStun()
				if pYou.mainCard.needsHeal() and pYou.mainCard.hasHeal() and pYou.mainCard.attacks[heal].staminaCost < pYou.mainCard.stamina:
					hasAttacked = pYou.attack(heal, pEne, self.textLog)
				#AI gets more stamina if it needs it and has the ability to
				elif pYou.mainCard.needsStamina() and pYou.mainCard.hasStaminaBoost() and pYou.mainCard.attacks[stamina].staminaCost < pYou.mainCard.stamina:
					hasAttacked = pYou.attack(stamina, pEne, self.textLog) 	
				#AI decides if it wants to stun enemy
				elif pYou.mainCard.hasStun() and not pEne.mainCard.isStunned() and random.random() < AIChanceToStun and pYou.mainCard.attacks[stun].staminaCost < pYou.mainCard.stamina:	
					hasAttacked = pYou.attack(stun, pEne, self.textLog)
				elif pYou.mainCard.name == "Clefable" and len(pYou.mainCard.findPossibleAttacks()) > 0:
					hasAttacked = self.clefable(pYou, pEne)
				elif len(pYou.mainCard.findPossibleAttacks()) > 0:
					hasAttacked = pYou.attack(calcAttack, pEne, self.textLog)
				else:
					print str(AICard)+" is too busy playing this awesome new Pokemongame..."
					print "He also lacks Stamina"
					self.textLog.append(str(AICard)+" lacks stamina"+"\n")
					if len(pYou.inv.invCards) == invCardsMax:
						throwaway = pYou.inv.getIndexOf(pYou.inv.invCards[randint(0,2)].name)
						if throwaway != -1:
							card = pYou.inv.remove(throwaway)
							hasAttacked = pYou.use(card, self.textLog)
					hasAttacked = True

		return hasAttacked			


# Usage: p = main.chooseCardAI(pYou,pEne):
# Before: pYou is active player and pEne is enemy player
# After: p is the pokemon pYou chooses(automatic)
def chooseCardAI(self, pYou, pEne):
		 chosen = str(pYou.hand.cards[0])
		 pokemon = pYou.hand.getNameOfNotWeakness(pEne.mainCard.poketype)
		 if(pokemon!="none"):
		 	chosen = pokemon
		 pokemon = pYou.hand.getNameOfResistance(pEne.mainCard.poketype)
		 if(pokemon!="none"):
		 	chosen = pokemon
		 pokemon = pYou.hand.getNameOfType(pEne.mainCard.weakness)
		 if(pokemon!="none"):
		 	chosen = pokemon
		 
		 ind = pYou.hand.getIndexOf(chosen)
		 
		 return pYou.hand.remove(ind)