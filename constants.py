#---------------------------------------------------
#				Other constants
#---------------------------------------------------
isLogged = False				#Tells you whethere you are writing log files to tell you about pokemons
loggedTurnsMax = 2000			#if you are logging the game it breaks after this many turns

#---------------------------------------------------
#	Constants that can be used to fine tune game
#---------------------------------------------------
resistanceMultiplier = 0.7		#how much % of damage a move does if the pokemon is resistant to that type of move
weaknessMultiplier = 1.3		#how much % of damage a move does if the pokemon is weak against that type of move
critChance = 0.1				#how likely it is that a pokemon crits
critMultiplier = 1.3			#how much % of damage a move does if it crits
missChance = 0.1				#chance that a move misses
typeEffectiveness = 0.7			#how much % of damage a move does if the pokemon is not that type, normal moves excluded
stunChance = 0.8				#chance that attacks with stun apply stun
stunChanceMin = 0.1				#chance that attacks with stun apply stun after the pokemon has been repeatedly stunned
turnsToMinStun = 10				#How many turns pokemon has to been stunned to reach minimum stun chance
metronomeAmount = 42			#Amount that metronome can range
metronomeBase = -20				#Starting amount for metronome
pointsToWin = 6					#points needed to win
needsHealMark = 0.35			#percentage of maxHealth to decide if pokemon needs healing
needsStaminaMark = 0.3			#percentage of maxStamina to decide if pokemon needs more stamina
stunSuccessRate = 0.1			#chance to make a successfull attack even though you are stunned
defEachTurn = 0.5				#amount the defence multiplier is raised by at the end of each of your turns
staminaEachRound = 7 			#amount of stamina regained each round
AIChanceToStun = 0.35 			#likelyhood of ai using stun providing he has a pokemon with stun and you are not already stunned
turnsBetweenInvCards = 3 		#turns between inventory cards; 3 means every 3rd turn, not every 4th turn(this only counts your turns, not opponent's)
#turnsToPenalty = 50				#turns untill pokemon recieves penalty for being too long on the field (this only counts your turns, not opponent's)
#defPenaltyMax =	0.3				#maximum defense penalty a card gets
#defPenaltyTime = 20				#turns untill penalty reaches penalty max (this only counts your turns, not opponent's)


#---------------------------------------------------
#		Constants that are not to be changed
#---------------------------------------------------
invCardsMax	= 3					#Maximum amount of inventory cards a player can have
cardsMax = 6					#Maximum amount of cards a player can hold
