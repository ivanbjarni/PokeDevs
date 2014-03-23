from Card import *
from Player import *
from Attack import *
import random
from Presets import *
import time 
from random import randint


class Main(object):	
	players = None			#Player[]	a list keeping track og the 2 players
	playerMode = "vs"		#String	 	player mode "vs" for 2 human players / "ai" for 1 human player and 1 computer
	turn = 0				#int 		states whether it is player's 0 turn or player's 1
	turnCount = 1			#int 		total number of turns passed
	waitingTime = 0			#int 		The time it takes the AI to choose attack each turn, random integral.


	def __init__(self, players):
		self.players = players
		
	def draw(self,pYou):
		#draw a new card if you can
		if not pYou.hand.isFull() and not pYou.deck.isEmpty():
			newCard = pYou.deck.draw()
			pYou.hand.add(newCard)				
			print "You draw a card. It's a "+str(newCard)

	def drawInv(self,pYou):
		#draw a new card if you can
		if not pYou.inv.isFull() and not pYou.invdeck.isEmpty():
			newCard = pYou.invdeck.draw()
			pYou.inv.add(newCard)				
			print "You draw a inventory card. It's a "+str(newCard)

	def chooseAttack(self,pYou, pEne):
		if pYou.isAI():
			self.chooseAttackAI(pYou, pEne)
		else:
			self.chooseAttackPlayer(pYou, pEne)

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
				hasUsed = pYou.use(card)
			elif x == "Back":
				print "Oh, so you're a tough guy?"
				hasUsed = True
			else:
				print "You don't have a inventorycard "+x+" in your hand."

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
						card = pYou.inv.remove(stamina)
						hasUsed = pYou.use(card)
						offset += 1
				elif pYou.inv.invCards[i].health > 0 and pYou.mainCard.needsHeal():
					print "I need heal"
					heal = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if heal != -1:
						card = pYou.inv.remove(heal)
						hasUsed = pYou.use(card)
						offset += 1
				elif pYou.inv.invCards[i].stun and pYou.mainCard.isStunned():
					print "I need to get unstunned"
					stun = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if stun != -1:
						card = pYou.inv.remove(stun)
						hasUsed = pYou.use(card)
						offset += 1
				elif pYou.inv.invCards[i].damageBoost > 1 and not pYou.mainCard.isStunned():
					print "I want to deal more DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card)
						offset += 1
				elif pYou.inv.invCards[i].defenseBoost > 0 and pYou.inv.invCards[i].defenseBoost < 1 and not pYou.mainCard.isStunned():
					print "I want to take less DAMAGE!!"
					damage = pYou.inv.getIndexOf(pYou.inv.invCards[i].name)
					if damage != -1:
						card = pYou.inv.remove(damage)
						hasUsed = pYou.use(card)
						offset += 1
			hasUsed = True			

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
				hasAttacked = pYou.attack(x-1,pEne)

	def chooseAttackAI(self, pYou, pEne):
		global waitingTime
		waitingTime = randint(2,5)
		time.sleep(waitingTime)			
		AICard = pYou.mainCard
		hasAttacked = False
		if len(pYou.inv.invCards) > 0:
			print "I have inventory things!"
			self.chooseInvCardAI(pYou, pEne)	
		#AI can't attack if his pokemon is stunned
		if AICard.isStunned():
			print str(AICard)+" is stunned"
			hasAttacked = True
		calcAttack = pYou.mainCard.findClosestAttack(pEne.mainCard.health) #Best attack choise for damage
		if pYou.mainCard.canKillEne(calcAttack, pEne.mainCard.health):
			hasAttacked = pYou.attack(calcAttack, pEne)
			print "I can kill you"
		else:
			while(not hasAttacked):	
				#AI checks if it needs to and can heal
				heal = pYou.mainCard.findHeal()
				stamina = pYou.mainCard.findStamina()
				stun = pYou.mainCard.findStun()
				if pYou.mainCard.needsHeal() and pYou.mainCard.hasHeal() and pYou.mainCard.attacks[heal].staminaCost < pYou.mainCard.stamina:
					hasAttacked = pYou.attack(heal, pEne)
				#AI gets more stamina if it needs it and has the ability to
				elif pYou.mainCard.needsStamina() and pYou.mainCard.hasStaminaBoost() and pYou.mainCard.attacks[stamina].staminaCost < pYou.mainCard.stamina:
					hasAttacked = pYou.attack(stamina, pEne) 	
				#AI decides if it wants to stun enemy
				elif pYou.mainCard.hasStun() and not pEne.mainCard.isStunned() and (randint(2,4) == 2) and pYou.mainCard.attacks[stun].staminaCost < pYou.mainCard.stamina:	
					hasAttacked = pYou.attack(stun, pEne)
				elif len(pYou.mainCard.findPossibleAttacks()) > 0:
					hasAttacked = pYou.attack(calcAttack, pEne)
				else:
					print str(AICard)+" is too busy playing this awesome new Pokemongame..."
					print "He also lacks Stamina"
					if len(pYou.inv.invCards) == 3:
						throwaway = pYou.inv.getIndexOf(pYou.inv.invCards[randint(0,2)].name)
						if throwaway != -1:
							card = pYou.inv.remove(throwaway)
							hasAttacked = pYou.use(card)
					hasAttacked = True

	# Usage: p = main.chooseCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses(automatic if pYou is AI, manual otherwise)
	def chooseCard(self, pYou, pEne):
		if pYou.isAI():
			return self.chooseCardAI(pYou, pEne)
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

	# Usage: p = main.chooseCardAI(pYou,pEne):
	# Before: pYou is active player and pEne is enemy player
	# After: p is the pokemon pYou chooses(automatic)
	def chooseCardAI(self,pYou, pEne):
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
			
	# Usage: p = drawInvQuest()
	# Before: Nothing
	# AFter: p is true if it is the right time to draw inventory card, false otherwise
	def drawInvQuest(self):
		if self.turnCount > 1:
			return (self.turnCount%5 == 0 or (self.turnCount - 1)%5 == 0)
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
			if(pYou.points>=pointsToWin):
				break

		if(self.players[0].points>self.players[1].points):
			print "Player 1 wins! With "+str(self.players[0].points)+" against "+str(self.players[1].points)
		elif(self.players[0].points<self.players[1].points):
			print "Player 2 wins! With "+str(self.players[1].points)+" against "+str(self.players[0].points)
		else:
			print "It's a draw, which basically means that Panda wins and both players lose!"