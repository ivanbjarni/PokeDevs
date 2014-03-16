from Deck import *
from Hand import *
from Card import *
from util import *
from InvCard import *


class Presets(object):
	invDecks	= []		#invDecks 	Predefined InvDecks of Invcards to be used
	invCards	= []		#
	decks		= []		#Decks		Predefined decks of cards to be used
	cards		= []		#Cards		Predefined cards to be used
	attacks 	= []		#Attacks 	Predefined attacks to be used


	def __init__(self):
		self.initInvCards()
		self.initAttacks()
		self.initCards()

	def __str__(self):
		return "presets"

	def initInvCards(self):
		self.invCards = {
		0	: InvCard("StaminaBoost1", 0, 15, False, 1),
		1	: InvCard("StaminaBoost2", 0, 25, False, 1),
		2	: InvCard("StaminaBoost3", 0, 35, False, 1),
		3	: InvCard("StaminaBoost4", 0, 45, False, 1),
		4	: InvCard("HealthPotion1", 10, 0, False, 1),
		5	: InvCard("HealthPotion2", 25, 0, False, 1),
		6	: InvCard("HealthPotion3", 40, 0, False, 1),
		7	: InvCard("HealthPotion4", 65, 0, False, 1),
		9	: InvCard("DamageBoost1", 0, 0, False, 1.2),
		10	: InvCard("DamageBoost2", 0, 0, False, 1.4),
		11	: InvCard("DamageBoost3", 0, 0, False, 1.6),
		12	: InvCard("DamageBoost4", 0, 0, False, 1.8),
		13	: InvCard("DoubleDamage", 0, 0, False, 2),
		14	: InvCard("LooseStun", 0, 0, True, 1),
		15	: InvCard("HealthAndStun", 20, 0, True, 1),
		16	: InvCard("StaminaAndStun", 0, 25, True, 1),
		17	: InvCard("TheWholePackage", 20, 20, True, 1.4)
		}

	def initAttacks(self):
		self.attacks ={
		0	: Attack("Empty", 0, 0, 0, 0, "normal"),				
		10	: Attack("Scratch", 10, 10, 0, 0, "normal"),			
		16	: Attack("Gust", 10, 10, 0, 0, "normal"),			
		17	: Attack("WingAttack", 15, 20, 0, 1, "normal"),			
		22	: Attack("VineWhip", 7, 10, 0, 0, "grass"),				
		31	: Attack("FuryAttack", 15, 25, 0, 1, "normal"),				
		32	: Attack("HornDrill", 25, 50, 0, 1, "normal"),				
		33	: Attack("Tackle", 7, 10, 0, 0, "normal"),				
		34	: Attack("BodySlam", 15, 30, 0, 0, "normal"),				
		36	: Attack("TakeDown", 10, 15, 0, 0, "normal"),			
		38	: Attack("DoubleEdge", 17, 22, 0, 0, "normal"),			
		39	: Attack("TailWhip", 10, 30, 0, 1, "normal"),			
		40	: Attack("PoisonSting", 15, 15, 0, 1, "normal"),			
		41	: Attack("Twineedle", 13, 20, 0, 0, "grass"),			
		44	: Attack("Bite", 15, 20, 0, 0, "normal"),				
		45	: Attack("Growl", 5, 5, 0, 0, "normal"),				
		47	: Attack("Sing", 0, 15, 0, 2, "normal"),				
		48	: Attack("Supersonic", 5, 30, 0, 2, "normal"),				
		51	: Attack("Acid", 10, 30, 0, 2, "grass"),				
		52	: Attack("Ember", 10, 10, 0, 0, "fire"),			
		53	: Attack("Flamethrower", 26, 30, 0, 0, "fire"),			
		55	: Attack("WaterGun", 18, 30, 0, 0, "water"),			
		56	: Attack("HydroPump", 50, 75, 0, 0, "water"),			
		61	: Attack("BubbleBeam", 28, 35, 0, 0, "water"),			
		64	: Attack("Peck", 12, 20, 0, 0, "normal"),			
		65	: Attack("DrillPeck", 32, 75, 0, 1, "normal"),			
		75	: Attack("RazorLeaf", 18, 30, 0, 0, "grass"),			
		76	: Attack("SolarBeam", 34, 80, 0, 0, "grass"),			
		80	: Attack("PetalDance", 15, 30, 0, 0, "grass"),			
		81	: Attack("StringShot", 10, 15, 0, 1, "grass"),			
		83	: Attack("FireSpin", 20, 35, 0, 0, "fire"),				
		84	: Attack("ThunderShock", 15, 30, 0, 0, "electric"),				
		85	: Attack("Thunderbolt", 30, 60, 0, 0, "electric"),				
		89	: Attack("Earthquake", 50, 90, 0, 0, "ground"),				
		91	: Attack("Dig", 0, -25, -20, 0, "ground"),				
		98	: Attack("QuickAttack", 12, 20, 0, 0, "normal"),	
		99	: Attack("Rage", 0, -20, -20, 2, "normal"),	
		106	: Attack("Harden", 0, -20, -30, 0, "normal"),	
		107	: Attack("Minimize", 0, -20, -30, 0, "normal"),	
		110 : Attack("Withdraw", 0, -17, -5, 0, "normal"),			
		114 : Attack("Haze", 0, -20, -20, 0, "water"),			
		116 : Attack("FocusEnergy", 0, -25, 0, 0, "normal"),	
		118 : Attack("Metronome", 0, 35, 0, 0, "normal"),	
		119 : Attack("MirrorMove", 0, -5, -25, 0, "normal"),	
		145 : Attack("Bubble", 10, 10, 0, 0, "water"),	
		158 : Attack("HyperFang", 17, 30, 0, 0, "water"),	
		210 : Attack("FuryCutter", 20, 40, 0, 0, "grass"),	
		219 : Attack("Safeguard", 0, 0, -25, 1, "normal"),	
		222 : Attack("Magnitude", 18, 30, 0, 1, "ground"),	
		222 : Attack("Megahorn", 30, 65, 5, 0, "grass"),	
		229 : Attack("RapidSpin", 7, 23, 0, 2,"normal"),			
		270 : Attack("HelpingHand", -30, 50, 0, 3, "normal"),			
		276 : Attack("Superpower", 7, -30, -20, 0, "normal"),			
		283 : Attack("Endeavor", 15, -20, -10, 2, "normal"),			
		304 : Attack("HyperVoice", 15, 30, 0, 0, "normal"),			
		305 : Attack("PoisonFang", 20, 40, 0, 2, "normal"),			
		318 : Attack("SilverWind", 20, 20, -10, 0, "grass"),			
		332 : Attack("AerialAce", 30, 0, 25, 0, "normal"),			
		352 : Attack("WaterPulse", 30, 30, 0, 0, "water"),			
		394 : Attack("FlareBlitz", 40, 50, 0, 0, "fire"),				
		403 : Attack("AirSlash", 25, 45, 0, 0, "normal"),				
		405 : Attack("BugBuzz", 35, 50, 0, 0, "grass"),				
		405 : Attack("EarthPower", 40, 60, 0, 1, "ground"),				
		424 : Attack("FireFang", 15, 12, 0, 2, "fire"),				
		426 : Attack("MudBomb", 20, 40, 0, 0, "normal"),				
		441 : Attack("GunkShot", 20, 60, 0, 2, "grass"),				
		441 : Attack("Captivate", 30, 60, 0, 0, "normal"),				
		450 : Attack("BugBite", 15, 15, 0, 2, "grass"),				
		486	: Attack("Thunder", 30, 50, 10, 0, "electric"),			
		491	: Attack("AcidSpray", 25, 50, 0, 0, "grass"),			
		491	: Attack("AfterYou", 0, 0, 0, 0, "normal"),			
		517	: Attack("Inferno", 25, 50, 0, 0, "fire"),				
		542	: Attack("Hurricane", 35, 60, 0, 1, "normal"),				
		565	: Attack("FellStinger", 30, 40, 10, 0, "grass"),				
		572	: Attack("PetalBlizzard", 35, 60, 0, 0, "grass"),
		572	: Attack("Moonblast", 25, 55, 0, 0, "normal"),
		678	: Attack("ElectroBall", 18, 30, 0, 0, "electric")
		

		}

	def initCards(self):
		self.cards = {
		1	: Card("Bulbasaur", 45, 90, [self.ga("Tackle"), self.ga("RazorLeaf"), self.ga("VineWhip"), self.ga("SolarBeam")], "grass", "fire", "water"),
		2   : Card("Ivysaur", 60, 80, [self.ga("TakeDown"), self.ga("RazorLeaf"), self.ga("DoubleEdge"), self.ga("SolarBeam")], "grass", "fire", "water"),
		3   : Card("Venusaur", 80, 82, [self.ga("VineWhip"), self.ga("PetalDance"), self.ga("SolarBeam"), self.ga("PetalBlizzard")], "grass", "fire", "water"),
		4	: Card("Charmander", 39, 100, [self.ga("Tackle"), self.ga("Growl"), self.ga("Flamethrower"), self.ga("Ember")], "fire", "water", "grass"),
		5	: Card("Charmeleon", 58, 90, [self.ga("Scratch"), self.ga("FireFang"), self.ga("Flamethrower"), self.ga("FireSpin")], "fire", "water", "grass"),
		6	: Card("Charizard", 78, 85, [self.ga("Ember"), self.ga("FireFang"), self.ga("Inferno"), self.ga("FlareBlitz")], "fire", "water", "grass"),
		7	: Card("Squirtle", 44, 90, [self.ga("Tackle"), self.ga("BubbleBeam"), self.ga("Withdraw"), self.ga("WaterGun")], "water", "grass", "fire"),
		8	: Card("Wartortle", 59, 100, [self.ga("Tackle"), self.ga("RapidSpin"), self.ga("Withdraw"), self.ga("WaterPulse")], "water", "grass", "fire"),
		9	: Card("Blastoise", 79, 105, [self.ga("Bubble"), self.ga("WaterPulse"), self.ga("WaterGun"), self.ga("HydroPump")], "water", "grass", "fire"),
		10	: Card("Caterpie", 45, 100, [self.ga("Tackle"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Empty")], "grass", "ground", "grass"),
		11	: Card("Metapod", 50, 120, [self.ga("Harden"), self.ga("Harden"), self.ga("Harden"), self.ga("Harden")], "grass", "ground", "grass"),
		12	: Card("Butterfree", 60, 110, [self.ga("Gust"), self.ga("Supersonic"), self.ga("SilverWind"), self.ga("BugBuzz")], "grass", "fire", "grass"),
		13	: Card("Weedle", 40, 60, [self.ga("PoisonSting"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Empty")], "grass", "ground", "grass"),
		14	: Card("Kakuna", 45, 80, [self.ga("Tackle"), self.ga("Harden"), self.ga("Harden"), self.ga("Harden")], "grass", "fire", "grass"),
		15	: Card("Beedrill", 65, 110, [self.ga("FocusEnergy"), self.ga("Twineedle"), self.ga("Rage"), self.ga("FellStinger")], "grass", "fire", "grass"),
		16	: Card("Pidgey", 40, 100, [self.ga("Tackle"), self.ga("Gust"), self.ga("WingAttack"), self.ga("AirSlash")], "normal", "electric", "grass"),
		17	: Card("Pidgeotto", 63, 105, [self.ga("Gust"), self.ga("WingAttack"), self.ga("AirSlash"), self.ga("Hurricane")], "normal", "electric", "grass"),
		18	: Card("Pidgeot", 83, 110, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("MirrorMove"), self.ga("Hurricane")], "normal", "electric", "grass"),
		19	: Card("Rattata", 30, 75, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("HyperFang"), self.ga("DoubleEdge")], "normal", "ground", "psychic"),
		20	: Card("Raticate", 55, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("DoubleEdge"), self.ga("Endeavor")], "normal", "ground", "psychic"),
		21	: Card("Spearow", 40, 85, [self.ga("Peck"), self.ga("Growl"), self.ga("FuryAttack"), self.ga("AerialAce")], "normal", "electric", "ground"),
		22	: Card("Fearow", 65, 100, [self.ga("Peck"), self.ga("MirrorMove"), self.ga("FuryAttack"), self.ga("DrillPeck")], "normal", "electric", "ground"),
		23	: Card("Ekans", 35, 75, [self.ga("PoisonSting"), self.ga("Acid"), self.ga("MudBomb"), self.ga("Haze")], "grass", "ground", "grass"),
		24	: Card("Arbok", 60, 95, [self.ga("PoisonSting"), self.ga("AcidSpray"), self.ga("GunkShot"), self.ga("Haze")], "grass", "psychic", "grass"),
		25	: Card("Pikachu", 35, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("ElectroBall"), self.ga("Thunder")], "electric", "ground", "electric"),
		26	: Card("Raichu", 60, 120, [self.ga("ThunderShock"), self.ga("QuickAttack"), self.ga("TailWhip"), self.ga("Thunderbolt")], "electric", "ground", "electric"),
		27	: Card("Sandshrew", 50, 80, [self.ga("Scratch"), self.ga("PoisonSting"), self.ga("Magnitude"), self.ga("Dig")], "ground", "water", "ground"),
		28	: Card("Sandslash", 75, 110, [self.ga("Scratch"), self.ga("FuryCutter"), self.ga("Earthquake"), self.ga("Dig")], "ground", "water", "ground"),
		29	: Card("NidoranF", 55, 80, [self.ga("Scratch"), self.ga("PoisonSting"), self.ga("TailWhip"), self.ga("PoisonFang")], "grass", "ground", "grass"),
		30	: Card("Nidorina", 70, 95, [self.ga("Scratch"), self.ga("HelpingHand"), self.ga("Captivate"), self.ga("PoisonFang")], "grass", "ground", "grass"),
		31	: Card("Nidoqueen", 90, 110, [self.ga("Scratch"), self.ga("BodySlam"), self.ga("EarthPower"), self.ga("Superpower")], "ground", "water", "grass"),
		32	: Card("NidoranM", 46, 89, [self.ga("Peck"), self.ga("PoisonSting"), self.ga("FocusEnergy"), self.ga("HelpingHand")], "grass", "ground", "grass"),
		33	: Card("Nidorino", 61, 105, [self.ga("PoisonSting"), self.ga("HelpingHand"), self.ga("Captivate"), self.ga("HornDrill")], "grass", "ground", "grass"),
		34	: Card("Nidoking", 81, 120, [self.ga("Peck"), self.ga("PoisonSting"), self.ga("EarthPower"), self.ga("Megahorn")], "ground", "water", "grass"),
		35	: Card("Clefairy", 70, 70, [self.ga("Sing"), self.ga("Metronome"), self.ga("Moonblast"), self.ga("AfterYou")], "normal", "grass", "ground"),
		36	: Card("Clefable", 95, 80, [self.ga("Sing"), self.ga("Metronome"), self.ga("Minimize"), self.ga("AfterYou")], "normal", "grass", "ground"),
		37	: Card("Vulpix", 38, 90, [self.ga("Ember"), self.ga("FireSpin"), self.ga("Captivate"), self.ga("Inferno")], "fire", "water", "grass"),
		38	: Card("Ninetales", 73, 105, [self.ga("QuickAttack"), self.ga("Flamethrower"), self.ga("Safeguard"), self.ga("Inferno")], "fire", "water", "grass"),
		39	: Card("Jigglypuff", 115, 70, [self.ga("Sing"), self.ga("BodySlam"), self.ga("HyperVoice"), self.ga("DoubleEdge")], "psychic", "ground", "psychic"),



		133	: Card("Eevee", 55, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("FocusEnergy"), self.ga("Bite")], "normal", "ground", "psychic")
		



		}

	#Short for get attack
	def ga(self, attack):
		if isNumber(attack):
			return self.attacks[attack]
		else:
			return self.getAttackByName(attack)

	def getAttackByName(self, string):
		for key, val in self.attacks.iteritems():
			if val.name == string:
				return val
		print "Attack not found: getAttackByName. attack: "+string
		return -1


	#Short for get Card
	def gc(self, card):
		if isNumber(card):
			return self.cards[card]
		else:
			return self.getCardByName(card)

	def getCardByName(self, string):
		for key, val in self.cards.iteritems():
			if val.name == string:
				return val
		print "card not found: getCardByName"
		return -1

	#Short for get invCard (short for inventory card)
	def gic(self, invCard):
		if isNumber(invCard):
			return self.invCards[invCard]
		else:
			return self.getInvCardByName(invCard)

	def getInvCardByName(self, string):
		for key, val in self.invCards.iteritems():
			if val.name == string:
				return val
		print "card not found: getCardByName"
		return -1