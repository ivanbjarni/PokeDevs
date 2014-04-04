from Card import *
from Player import *
from Attack import *
from AI import *
import random
from Presets import *
import time 
from random import randint
from constants import *

class Main(object):	
	players = None			#Player[]	a list keeping track og the 2 players
	playerMode = "vs"		#String	 	player mode "vs" for 2 human players / "ai" for 1 human player and 1 computer
	textLog = []			#List       Grabs all of the printed text to output what is going on in the game
	turn = 0				#int 		states whether it is player's 0 turn or player's 1
	turnCount = 1			#int 		total number of turns passed
	waitingTime = 0			#int 		The time it takes the AI to choose attack each turn, random integral.

	def __init__(self, players):
		self.players = players

	
	# Usage: main.draw(pYou)
	# Before: pYou is active player                         
	# After: pYou has drawn a pokemoncard             	
	def draw(self,pYou):
		#draw a new card if you can
		if not pYou.hand.isFull() and not pYou.deck.isEmpty():
			newCard = pYou.deck.draw()
			pYou.hand.add(newCard)				
			print "You draw a card. It's a "+str(newCard)
			if pYou.isAI():
				self.textLog.append("Opponent draws a card.\n")
			else:
				self.textLog.append("You draw a card. It's a "+str(newCard)+"\n")

	
	# Usage: main.drawInv(pYou)
	# Before: pYou is active player                         
	# After: pYou has drawn an Inventorcard.		
	def drawInv(self,pYou):
		#draw a new card if you can
		if not pYou.inv.isFull() and not pYou.invdeck.isEmpty():
			newCard = pYou.invdeck.draw()
			pYou.inv.add(newCard)
			print "You draw a inventory card. It's a "+str(newCard)
			if pYou.isAI():
				self.textLog.append("Opponent draws an inventory card\n")
			else:
				self.textLog.append("You draw an inventory card. It's a "+str(newCard)+"\n")

	# Code for AI so it only uses HelpingHand at the right times
	def HelpingHand(self, pYou, pEne, stun):
		if pEne.mainCard.health < pEne.mainCard.healthMax * 0.9 and pYou.mainCard.attacks[stun].name == "HelpingHand":
			return False
		else:
			return True

	#Checks if the staminaboost of maincard could be fatal
	def notdie(self, pYou):
		if pYou.mainCard.hasStaminaBoost():
			sboost = pYou.mainCard.findStamina()
			if pYou.mainCard.attacks[sboost].healthCost > 0 and pYou.mainCard.health < 0.5 * pYou.mainCard.healthMax:
				return False
			else:
				return True
		else:
			return True

	#AI decides if it will stun the opponent
	def willstun(self, pYou, pEne, stun):
		if pYou.mainCard.hasStun() and not pEne.mainCard.isStunned() and random.random() < AIChanceToStun and pYou.mainCard.attacks[stun].staminaCost < pYou.mainCard.stamina and self.HelpingHand(pYou, pEne, stun):
			return True
		else:
			return False	

	#AI checks if it needs to and can heal
	def willheal(self, pYou, heal):		
		if pYou.mainCard.needsHeal() and pYou.mainCard.hasHeal() and pYou.mainCard.attacks[heal].staminaCost < pYou.mainCard.stamina:
			return True
		else:
			return False		

	#AI checks if it needs to and can increase stamina
	def willstaminaboost(self, pYou, stamina):
		if pYou.mainCard.needsStamina() and pYou.mainCard.hasStaminaBoost() and pYou.mainCard.attacks[stamina].staminaCost < pYou.mainCard.stamina and self.notdie(pYou):
			return True
		else:
			return False 

	#Code for AI so it uses Metronome, given the chanse to.
	def clefable(self, pYou, pEne):
		calcAttack = pYou.mainCard.findClosestAttack(pEne.mainCard.health)   
		for x in range(0,4):
			if pYou.mainCard.attacks[x].name == "Metronome" and pYou.mainCard.attacks[x].staminaCost < pYou.mainCard.stamina:
				calcAttack = x
		return pYou.attack(calcAttack, pEne, self.textLog)

	# Usage: main.chooseInvCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: The AI chooses what inventorycard to use based on "logic"	
	def chooseInvCardAI(self, pYou, pEne):
		yourCard = pYou.mainCard
		hasUsed = False 
		while(not hasUsed):
			heal = pYou.mainCard.findHeal()
			stamina = pYou.mainCard.findStamina()
			stun = pYou.mainCard.findStun()
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
				elif not pYou.mainCard.hasDmgBoost() and pYou.inv.invCards[i].damageBoost > 1 and not pYou.mainCard.isStunned() and pYou.mainCard.health >  pYou.inv.invCards[i].health*(-2) and not self.willheal(pYou, heal) and not self.willstaminaboost(pYou, stamina):
					print "I want to deal more DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						self.textLog.append("Opponent uses an inventory card to deal more damage\n")						
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif not pYou.mainCard.hasDefBoost() and pYou.inv.invCards[i].defenseBoost > 0 and pYou.inv.invCards[i].defenseBoost < 1 and not pYou.mainCard.health < 15:
					print "I want to take less DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						self.textLog.append("Opponent uses an inventory card to take less damage\n")						
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card, self.textLog)
						offset += 1
				elif not pYou.mainCard.hasWeakExploit() and pYou.inv.invCards[i].weakExploit > 0 and pEne.mainCard.weakness == pYou.mainCard.poketype:
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


	# Usage: main.chooseAttackAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: The AI chooses what to do based on "logic"
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
				heal = pYou.mainCard.findHeal()
				stamina = pYou.mainCard.findStamina()
				stun = pYou.mainCard.findStun()
				#AI checks if it needs to and can heal
				if self.willheal(pYou, heal):
					hasAttacked = pYou.attack(heal, pEne, self.textLog)
				#AI gets more stamina if it needs it and has the ability to
				elif self.willstaminaboost(pYou, stamina):
					hasAttacked = pYou.attack(stamina, pEne, self.textLog) 	
				#AI decides if it wants to stun enemy
				elif self.willstun(pYou, pEne, stun):	
					hasAttacked = pYou.attack(stun, pEne, self.textLog)
				elif (pYou.mainCard.name == "Clefable" or pYou.mainCard.name == "Clefairy") and len(pYou.mainCard.findPossibleAttacks()) > 0:
					hasAttacked = self.clefable(pYou, pEne)
				elif len(pYou.mainCard.findPossibleAttacks()) > 0:
					if pYou.mainCard.attacks[calcAttack].stun > 0 and pEne.mainCard.isStunned():
						print "Well, I'm collecting stamina"
						hasAttacked = True
					elif pYou.mainCard.health > pYou.mainCard.healthMax * 0.85 and pYou.mainCard.attacks[calcAttack].healthCost < 0 and pYou.mainCard.attacks[calcAttack].damage == 0:
						print "Well, I'm collecting stamina"
						hasAttacked = True
					elif pYou.mainCard.stamina > pYou.mainCard.staminaMax * 0.85 and pYou.mainCard.attacks[calcAttack].staminaCost < 0  and pYou.mainCard.attacks[calcAttack].damage == 0:
						print "Well, I'm collecting stamina"
						hasAttacked = True
					elif pEne.mainCard.health < pEne.mainCard.healthMax * 0.9 and pYou.mainCard.attacks[calcAttack].name == "HelpingHand":
						print "Well, I'm collecting stamina"
						hasAttacked = True
					else:
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

	
	# Usage: main.chooseAttackAIrandom(pYou, pEne):
	# Before: pYou is active player and pEne is enemy player
	# After:  The AI picks some random attack
	def chooseAttackAIrandom(self, pYou, pEne):
		AICard = pYou.mainCard
		hasAttacked = False
		arasir = len(pYou.mainCard.findPossibleAttacks())
		if len(pYou.inv.invCards) > 0:
			print "I have inventory things!"
			self.chooseInvCardAI(pYou, pEne)	
		#AI can't attack if his pokemon is stunned
		if AICard.isStunned():
			print str(AICard.name)+" is stunned"
			self.textLog.append(str(AICard)+" is stunned\n")
			hasAttacked = True
		elif arasir > 0:
			hasAttacked = pYou.attack(randint(0,arasir-1), pEne, self.textLog)
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

	

	# Usage: main.chooseCardAIrandom(pYou, pEne, number):
	# Before: pYou is active player and pEne is enemy player.
	# After: AI chooses a random card from hand. 
	def chooseCardAIrandom(self, pYou, pEne):
		howmany = len(pYou.hand.cards)
		IPickYou = randint(0, howmany-1)
		chosen = str(pYou.hand.cards[IPickYou])
		ind = pYou.hand.getIndexOf(chosen)
		return pYou.hand.remove(ind)


	# Usage: main.chooselogic(pYou, pEne, number):
	# Before: pYou is active player and pEne is enemy player, number is some integer between 0 and 10
	# After: If playername is computer, the AI chooses next attack for player.
	#		If not, the game waits for input from human player.
	def chooselogic(self, pYou, pEne, number, logic):
		decision = randint(0,11)
		if(decision > number and logic == "attack"):
			return self.chooseAttackAIrandom(pYou, pEne)
		elif(decision <= number and logic == "attack"):
			return self.chooseAttackAI(pYou, pEne)
		elif(decision > number and logic == "card"):
			return self.chooseCardAIrandom(pYou, pEne)
		elif(decision <= number and logic == "card"):
			return self.chooseCardAI(pYou, pEne)


	# Usage: main.chooseAttack(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: The computer either chooses a random attack or a logical one
	def chooseAttack(self,pYou, pEne):
		if pYou.isAI():
			self.chooseAttackAI(pYou, pEne)
		elif pYou.isAIEasy():
			self.chooselogic(pYou, pEne, 4, "attack")
		elif pYou.isAINormal():
			self.chooselogic(pYou, pEne, 7, "attack" )	
		else:
			self.chooseAttackPlayer(pYou, pEne)

	
	# Usage: main.chooseInvCardPlayer(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: The chosen inventorycard has been applied to main card		
	def chooseInvCardPlayer(self, pYou, pEne):
		yourCard = pYou.mainCard
		hasUsed = False
		while(not hasUsed):
			print "Your inventory: "+str(pYou.inv)
			print "What item do you wan't to use? (Back to go back)"
			x = raw_input()
			ind = pYou.inv.getIndexOf(x)
			if ind != -1:
				card = pYou.inv.remove(ind)
				hasUsed = pYou.use(card, self.textLog)
			elif x == "Back":
				print "Oh, so you're a tough guy?"
				hasUsed = True
			else:
				print "You don't have a inventorycard "+x+" in your hand."
	
	# Usage: p = main.chooseCardPlayer(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses
	def chooseAttackPlayer(self, pYou, pEne):
		yourCard = pYou.mainCard
		hasAttacked = False
		while(not hasAttacked):
			print 'What attack do you want to do 1-4? (0 to pass, 5 to access inventory, other to crash game): ',
			x = input()
			if x == 5:
				if len(pYou.inv.invCards) > 0:
					self.chooseInvCardPlayer(pYou, pEne)
				else:
					print "You don't have any inventorycards!"
			elif x == 0:
				print "You passed on your turn"
				hasAttacked = True
			elif x==9:
				yourCard.health -= 9000
				print "You chose self inflected damage, "+str(yourCard)+" loses 9000hp"
				hasAttacked = True
			else:
				hasAttacked = pYou.attack(x-1,pEne, self.textLog)



	# Usage: p = main.chooseCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses(automatic)
	def chooseCardAI(self, pYou, pEne):
		 chosen = pYou.hand.getNameOfHighestStats()
		 pokemon = pYou.hand.getNameOfNotWeakness(pEne.mainCard.poketype)
		 if(pokemon!="none"):
		 	chosen = pokemon
		 pokemon = pYou.hand.getNameOfResistance(pEne.mainCard.poketype)
		 if(pokemon!="none" and pYou.mainCard.poketype != pEne.mainCard.resistance):
		 	chosen = pokemon
		 pokemon = pYou.hand.getNameOfType(pEne.mainCard.weakness)
		 if(pokemon!="none" and pYou.mainCard.weakness != pEne.mainCard.poketype):
		 	chosen = pokemon
		 print "chose: "+str(ind)+"("+str(chosen)+")"
		 ind = pYou.hand.getIndexOf(chosen)
		 
		 return pYou.hand.remove(ind)

	# Usage: p = main.chooseCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses(automatic if pYou is AI, manual otherwise)
	def chooseCard(self, pYou, pEne):
		if pYou.isAI():
			return self.chooseCardAI(pYou, pEne)
		elif pYou.isAIEasy():
			#return self.chooseCardAIrandom(pYou, pEne)
			return self.chooselogic(pYou, pEne, 4, "card" )
		elif pYou.isAINormal():
			#return self.chooseCardAIrandom(pYou, pEne)
			return self.chooselogic(pYou, pEne, 7, "card")	
		else:
			return self.chooseCardPlayer(pYou, pEne)

	# Usage: p = main.chooseCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses(manual)
	def chooseCardPlayer(self,pYou, pEne):
		while(True):
			print 'What pokemon do you want to put out:',
			inp = raw_input()
			ind = pYou.hand.getIndexOf(inp)
			if ind != -1:
				return pYou.hand.remove(ind)
			else:
				print "You don't have a pokemon named "+inp+" in your hand."

			
	# Usage: p = drawInvQuest()
	# Before: Nothing
	# AFter: p is true if it is the right time to draw inventory card, false otherwise
	def drawInvQuest(self):
		if self.turnCount > 1:
			return (self.turnCount%(2*turnsBetweenInvCards) == 0 or (self.turnCount - 1)%(2*turnsBetweenInvCards) == 0)
		else:
			return False

	def gameLoop(self):
		done = False
		presets = Presets()
		while(not done):
			# define new variables for short
			t = self.turn
			pYou = self.players[t]			#player you
			pEne = self.players[(t+1)%2]	#player enemy
			yourCard = pYou.mainCard
			enemCard = pEne.mainCard

			#remove 1 point so you don't get an extra point if the enemy was already dead
			if pEne.mainCard.isDead():
				pYou.points -= 1

			# print stuff about turns
			print "\n\n\n\n"
			print "Total turns:" + str(self.turnCount)
			print "It's player's "+str(t+1)+" turn."

			#Draw a new card in the start of your turn
			self.draw(pYou)
			if self.drawInvQuest():
				self.drawInv(pYou)
		
			
			print "Your Hand: "+str(pYou.hand)
			print "Your Inventory: "+str(pYou.inv)

			#put out a new pokemon
			if yourCard.isDead():
				pYou.graveyard.add(yourCard)
				newCard = self.chooseCard(pYou,pEne)
				#Tell player a pokemon is being swithced and switch pokemons
				print str(yourCard) + " come back, "+str(newCard)+" I choose you!"
				yourCard = newCard
				if isLogged:
					pokemonCounterLog(str(newCard),"pokemonPlayed.txt")
				pYou.mainCard = newCard


			#Print info about what is going on on the field
			print "Enemy pokemon is:",
			print enemCard.shortInfo()
			print "Your pokemon is:",
			print yourCard.shortInfo()
			print "Attacks:"
			print yourCard.getAttacks()

			# Let player choose attack
			self.chooseAttack(pYou,pEne)

			yourCard.applyEffects()
			
			# update turns and stuff afterwards
			self.turn = (t+1)%2
			self.turnCount+=1

			#Update points
			if pEne.mainCard.isDead():
				pYou.points += 1
			if pYou.mainCard.isDead():
				pEne.points += 1
			#end game if you have enough points
			if(pYou.points>=pointsToWin or (isLogged and self.turnCount > loggedTurnsMax)):
				break

		if(self.players[0].points>self.players[1].points):
			print "Player 1 wins! With "+str(self.players[0].points)+" against "+str(self.players[1].points)
		elif(self.players[0].points<self.players[1].points):
			print "Player 2 wins! With "+str(self.players[1].points)+" against "+str(self.players[0].points)
		else:
			print "It's a draw, which basically means that Panda wins and both players lose!"