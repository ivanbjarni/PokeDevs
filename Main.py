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
				hasUsed = pYou.use(card, self.textLog)
			elif x == "Back":
				print "Oh, so you're a tough guy?"
				hasUsed = True
			else:
				print "You don't have a inventorycard "+x+" in your hand."


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