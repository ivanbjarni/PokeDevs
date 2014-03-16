from Card import *
from Player import *
from Attack import *
import random


class Main(object):	
	players = None			#Player[]	a list keeping track og the 2 players
	playerMode = "vs"		#String	 	player mode "vs" for 2 human players / "ai" for 1 human player and 1 computer
	turn = 1				#int 		states whether it is player's 0 turn or player's 1
	turnCount = 1			#int 		total number of turns passed

	def __init__(self, players):
		self.players = players
		

	def gameLoop(self):
		done = False
		while(not done):
			# define new variables for short
			t = self.turn
			yourCard = self.players[t].mainCard
			enemCard = self.players[(t+1)%2].mainCard

			# print ALL the things
			print "\n\n\n\n"
			print "Total turns:" + str(self.turnCount)
			print "It's player's "+str(t)+" turn."
			print "Enemy pokemon is: "+str(enemCard)+" (hp:"+str(enemCard.health)+"/"+str(enemCard.healthMax)+"sta:"+str(enemCard.stamina)+"/"+str(enemCard.staminaMax)+")"
			print "Your pokemon is:"  +str(yourCard)+" (hp:"+str(yourCard.health)+"/"+str(yourCard.healthMax)+"sta:"+str(yourCard.stamina)+"/"+str(yourCard.staminaMax)+")"
			print "Attacks:"
			print yourCard.getAttacks()

			# Let player choose attack
			hasAttacked = False
			while(not hasAttacked):
				print 'What attack do you want to do',
				x = input()
				hasAttacked = self.players[t].attack(x,self.players[(t+1)%2])

			
			# update turns and stuff afterwards
			self.turn = (t+1)%2
			self.turnCount+=1