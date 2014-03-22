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

	def chooseAttack(self,pYou, pEne):
		if pYou.isAI():
			self.chooseAttackAI(pYou, pEne)
		else:
			self.chooseAttackPlayer(pYou, pEne)

	def chooseAttackPlayer(self, pYou, pEne):
		yourCard = pYou.mainCard
		hasAttacked = False
		while(not hasAttacked):
			print 'What attack do you want to do 1-4 (0 to pass, other to crash game): ',
			x = input()
			if x == 0:
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
		waitingTime = randint(2,8)
		time.sleep(waitingTime)			
		AICard = pYou.mainCard
		hasAttacked = False
		#AI can't attack if his pokemon is stunned
		if AICard.isStunned():
			print str(AICard)+" is stunned"
			hasAttacked = True
		else:	
			#AI checks if it needs to and can heal	
			if pYou.mainCard.needsHeal():
				heal = pYou.mainCard.findHeal()
				hasAttacked = pYou.attack(heal, pEne)
			#AI gets more stamina if it needs it and has the ability to
			if pYou.mainCard.needsStamina():
				stamina = pYou.mainCard.findStamina()
				hasAttacked = pYou.attack(stamina, pEne) 	
		 	if len(pYou.mainCard.findPossibleAttacks()) > 0:
			 	print pEne.mainCard.health
			 	calcAttack = pYou.mainCard.findClosestAttack(pEne.mainCard.health)
			 	hasAttacked = pYou.attack(calcAttack, pEne)
			else:
				print str(AICard)+" is too busy playing this awesome new Pokemongame..."
				print "He also lacks Stamina"


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
			
			print "Your Hand: "+str(pYou.hand)

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