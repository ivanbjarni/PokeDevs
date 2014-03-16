from Card import *
from Player import *
from Attack import *
import random
from Presets import *

class Main(object):	
	players = None			#Player[]	a list keeping track og the 2 players
	playerMode = "vs"		#String	 	player mode "vs" for 2 human players / "ai" for 1 human player and 1 computer
	turn = 0				#int 		states whether it is player's 0 turn or player's 1
	turnCount = 1			#int 		total number of turns passed

	def __init__(self, players):
		self.players = players
		

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

			# print stuff about turns
			print "\n\n\n\n"
			print "Total turns:" + str(self.turnCount)
			print "It's player's "+str(t+1)+" turn."

			#draw a new card if you can
			if not pYou.hand.isFull():
				pYou.hand.add(presets.gc(random.randrange(1, 19, 1)))

			print "Your Hand: "+str(pYou.hand)

			#put out a new pokemon
			if yourCard.isDead():
				pYou.graveyard.add(yourCard)
				hasChosen = False
				while(not hasChosen):
					print 'What pokemon do you want to put out:',
					inp = raw_input()
					ind = pYou.hand.getIndexOf(inp)
					if ind != -1:

						newCard = pYou.hand.remove(ind)
						hasChosen = True
					else:
						print "You don't have a pokemon named "+inp+" in your hand."
				#Tell player a pokemon is being swithced and switch pokemons
				print str(yourCard) + " come back, "+str(newCard)+" I choose you!"
				yourCard = newCard
				pYou.mainCard = newCard


			#Print info about what is going on on the field
			print "Enemy pokemon is: "+str(enemCard)+" (hp:"+str(enemCard.health)+"/"+str(enemCard.healthMax)+" sta:"+str(enemCard.stamina)+"/"+str(enemCard.staminaMax)+")"
			print "Your pokemon is:"  +str(yourCard)+" (hp:"+str(yourCard.health)+"/"+str(yourCard.healthMax)+" sta:"+str(yourCard.stamina)+"/"+str(yourCard.staminaMax)+")"
			print "Attacks:"
			print yourCard.getAttacks()

			# Let player choose attack
			hasAttacked = False
			while(not hasAttacked):
				print 'What attack do you want to do 1-4 (0 to pass, other to crash game): ',
				x = input()
				if x == 0:
					print "You passed on your turn"
					hasAttacked = True
				elif x==9:
					yourCard.health -= 9000
					print "You chose self inflected damage "+str(yourCard)+" loses 9000hp"
					hasAttacked = True
				else:
					hasAttacked = pYou.attack(x-1,pEne)


			
			# update turns and stuff afterwards
			self.turn = (t+1)%2
			self.turnCount+=1