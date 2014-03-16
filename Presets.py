from Deck import *
from Hand import *
from Card import *
from util import *


class Presets(object):
	decks		= []		#Decks		Predefined cecks of cards to be used
	cards		= []		#Cards		Predefined cards to be used
	attacks 	= []		#Attacks 	Predefined attacks to be used

	def __init__(self):
		self.initAttacks()
		self.initCards()

	def __str__(self):
		return "presets"

	def initAttacks(self):
		self.attacks ={
		0	: Attack("Empty", 0, 0, 0, 0, "normal"),				
		2	: Attack("KarateChop", 25, 25, 0, 0, "ground"),				
		3	: Attack("DoubleSlap", 20, 40, 0, 0, "normal"),				
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
		46	: Attack("Roar", 7, 5, 0, 0, "normal"),				
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
		67	: Attack("Low Kick", 15, 15, 0, 0, "ground"),			
		71	: Attack("Absorb", 15, 20, -15, 0, "grass"),			
		72	: Attack("MegaDrain", 22, 25, -22, 0, "grass"),			
		75	: Attack("RazorLeaf", 18, 30, 0, 0, "grass"),			
		76	: Attack("SolarBeam", 34, 65, 0, 0, "grass"),			
		79	: Attack("SleepPowder", 0, 20, 0, 1, "grass"),			
		80	: Attack("PetalDance", 15, 30, 0, 0, "grass"),			
		81	: Attack("StringShot", 10, 15, 0, 1, "grass"),			
		83	: Attack("FireSpin", 20, 35, 0, 0, "fire"),				
		84	: Attack("ThunderShock", 15, 30, 0, 0, "electric"),				
		85	: Attack("Thunderbolt", 30, 60, 0, 0, "electric"),				
		89	: Attack("Earthquake", 50, 90, 0, 0, "ground"),				
		90	: Attack("Fissure", 40, 100, 0, 1, "ground"),				
		91	: Attack("Dig", 0, -25, -20, 1, "ground"),				
		98	: Attack("QuickAttack", 12, 20, 0, 0, "normal"),	
		99	: Attack("Rage", 0, -20, -20, 2, "normal"),	
		106	: Attack("Harden", 0, -20, -30, 0, "normal"),	
		107	: Attack("Minimize", 0, -20, -30, 0, "normal"),	
		110 : Attack("Withdraw", 0, -17, -5, 0, "normal"),			
		114 : Attack("Haze", 0, -20, -20, 0, "water"),			
		116 : Attack("FocusEnergy", 0, -25, 0, 0, "normal"),	
		118 : Attack("Metronome", 0, 0, 0, 0, "normal"),	
		119 : Attack("MirrorMove", 0, -5, -25, 0, "normal"),	
		141 : Attack("LeechLife", 15, 30, -15, 0, "normal"),	
		145 : Attack("Bubble", 10, 10, 0, 0, "water"),	
		158 : Attack("HyperFang", 17, 30, 0, 0, "water"),	
		163 : Attack("Slash", 20, 40, 0, 0, "normal"),	
		172 : Attack("FlameWheel", 20, 40, 0, 0, "fire"),	
		202 : Attack("GigaDrain", 30, 60, -30, 0, "grass"),	
		207 : Attack("Swagger", 0, -50, 0, 0, "normal"),	
		210 : Attack("FuryCutter", 20, 40, 0, 0, "grass"),	
		219 : Attack("Safeguard", 0, 0, -25, 1, "normal"),	
		222 : Attack("Magnitude", 18, 30, 0, 1, "ground"),	
		224 : Attack("Megahorn", 30, 65, 5, 0, "grass"),	
		229 : Attack("RapidSpin", 7, 23, 0, 2, "normal"),			
		229 : Attack("CrossChop", 33, 60, 0, 1, "ground"),			
		252 : Attack("FakeOut", 12, 14, 0, 0, "normal"),			
		270 : Attack("HelpingHand", -30, 50, 0, 2, "normal"),			
		276 : Attack("Superpower", 7, -30, -20, 0, "normal"),			
		283 : Attack("Endeavor", 15, -20, -10, 2, "normal"),			
		304 : Attack("HyperVoice", 15, 30, 0, 0, "normal"),			
		305 : Attack("PoisonFang", 20, 40, 0, 2, "normal"),			
		318 : Attack("SilverWind", 20, 20, -10, 0, "grass"),			
		324 : Attack("SignalBeam", 15, 28, 0, 0, "grass"),			
		332 : Attack("AerialAce", 30, 0, 25, 0, "normal"),			
		352 : Attack("WaterPulse", 30, 30, 0, 0, "water"),			
		364 : Attack("Feint", 0, -15, -30, 0, "normal"),			
		370 : Attack("CloseCombat", 30, 50, 0, 0, "normal"),			
		394 : Attack("FlareBlitz", 40, 50, 0, 0, "fire"),				
		403 : Attack("AirSlash", 25, 45, 0, 0, "normal"),				
		404 : Attack("X-Scissor", 30, 50, 0, 0, "grass"),				
		405 : Attack("BugBuzz", 35, 50, 0, 0, "grass"),				
		414 : Attack("EarthPower", 40, 60, 0, 1, "ground"),				
		422 : Attack("ThunderFang", 15, 12, 0, 1, "electric"),				
		424 : Attack("FireFang", 15, 12, 0, 1, "fire"),				
		426 : Attack("MudBomb", 20, 40, 0, 0, "normal"),				
		428 : Attack("ZenHeadbutt", 10, -30, 0, 0, "psychic"),				
		441 : Attack("GunkShot", 20, 60, 0, 2, "grass"),				
		445 : Attack("Captivate", 30, 60, 0, 0, "normal"),				
		450 : Attack("BugBite", 15, 15, 0, 2, "grass"),				
		472 : Attack("WonderRoom", 0, 15, -10, 1, "psychic"),				
		486	: Attack("Thunder", 30, 50, 10, 0, "electric"),			
		491	: Attack("AcidSpray", 25, 50, 0, 0, "grass"),			
		495	: Attack("AfterYou", 0, 0, 0, 0, "normal"),			
		512	: Attack("Acrobatics", 20, 45, 0, 0, "normal"),			
		512	: Attack("FinalGambit", 40, 0, 25, 0, "normal"),			
		517	: Attack("Inferno", 25, 50, 0, 0, "fire"),				
		542	: Attack("Hurricane", 35, 60, 0, 1, "normal"),				
		565	: Attack("FellStinger", 30, 40, 10, 0, "grass"),				
		572	: Attack("PetalBlizzard", 35, 60, 0, 0, "grass"),
		580	: Attack("GrassyTerrain", 0, 50, -30, 0, "grass"),
		583	: Attack("PlayRough", 27, 55, 0, 0, "normal"),
		585	: Attack("Moonblast", 25, 55, 0, 0, "normal"),
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
		11	: Card("Metapod", 50, 12000, [self.ga("Harden"), self.ga("Harden"), self.ga("Harden"), self.ga("Harden")], "grass", "ground", "grass"),
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
		39	: Card("Jigglypuff", 115, 70, [self.ga("Sing"), self.ga("BodySlam"), self.ga("HyperVoice"), self.ga("DoubleEdge")], "normal", "ground", "psychic"),
		40	: Card("Wigglytuff", 140, 85, [self.ga("Sing"), self.ga("PlayRough"), self.ga("DoubleSlap"), self.ga("DoubleEdge")], "normal", "grass", "psychic"),
		41	: Card("Zubat", 40, 80, [self.ga("LeechLife"), self.ga("WingAttack"), self.ga("PoisonFang"), self.ga("Haze")], "normal", "electric", "ground"),
		42	: Card("Zubat", 75, 90, [self.ga("LeechLife"), self.ga("Acrobatics"), self.ga("PoisonFang"), self.ga("AirSlash")], "normal", "electric", "ground"),
		43	: Card("Oddish", 45, 85, [self.ga("Absorb"), self.ga("Acid"), self.ga("SleepPowder"), self.ga("PetalDance")], "grass", "fire", "water"),
		44	: Card("Gloom", 60, 95, [self.ga("Absorb"), self.ga("PetalBlizzard"), self.ga("GrassyTerrain"), self.ga("PetalDance")], "grass", "fire", "water"),
		45	: Card("Vileplume", 75, 105, [self.ga("MegaDrain"), self.ga("PetalBlizzard"), self.ga("SolarBeam"), self.ga("PetalDance")], "grass", "fire", "water"),
		46	: Card("Paras", 35, 70, [self.ga("Scratch"), self.ga("LeechLife"), self.ga("FuryCutter"), self.ga("GigaDrain")], "grass", "fire", "ground"),
		47	: Card("Parasect", 60, 90, [self.ga("LeechLife"), self.ga("FuryCutter"), self.ga("GigaDrain"), self.ga("X-Scissor")], "grass", "fire", "ground"),
		48	: Card("Venonat", 60, 80, [self.ga("Tackle"), self.ga("Supersonic"), self.ga("SignalBeam"), self.ga("PoisonFang")], "grass", "fire", "grass"),
		49	: Card("Venomoth", 70, 100, [self.ga("BugBuzz"), self.ga("Gust"), self.ga("SignalBeam"), self.ga("PoisonFang")], "grass", "fire", "grass"),
		50	: Card("Diglett", 10, 100, [self.ga("Dig"), self.ga("EarthPower"), self.ga("Magnitude"), self.ga("Earthquake")], "ground", "water", "electric"),
		51	: Card("Dugtrio", 35, 150, [self.ga("Dig"), self.ga("EarthPower"), self.ga("Earthquake"), self.ga("Fissure")], "ground", "water", "electric"),
		52	: Card("Meowth", 40, 75, [self.ga("Scratch"), self.ga("FakeOut"), self.ga("Slash"), self.ga("Feint")], "normal", "ground", "psychic"),
		53	: Card("Persian", 65, 105, [self.ga("Scratch"), self.ga("Captivate"), self.ga("Slash"), self.ga("Feint")], "normal", "ground", "psychic"),
		54	: Card("Psyduck", 50, 80, [self.ga("Scratch"), self.ga("ZenHeadbutt"), self.ga("TailWhip"), self.ga("HydroPump")], "psychic", "water", "electric"),
		55	: Card("Golduck", 80, 100, [self.ga("WaterGun"), self.ga("ZenHeadbutt"), self.ga("WonderRoom"), self.ga("HydroPump")], "psychic", "water", "electric"),
		56	: Card("Mankey", 40, 70, [self.ga("LowKick"), self.ga("Swagger"), self.ga("KarateChop"), self.ga("CloseCombat")], "ground", "psychic", "grass"),
		57	: Card("Primeape", 65, 90, [self.ga("LowKick"), self.ga("Swagger"), self.ga("CrossChop"), self.ga("FinalGambit")], "ground", "psychic", "grass"),
		58	: Card("Growlithe", 55, 80, [self.ga("Ember"), self.ga("FlameWheel"), self.ga("Flamethrower"), self.ga("HelpingHand")], "fire", "water", "grass"),
		59	: Card("Arcanine", 90, 90, [self.ga("Roar"), self.ga("ThunderFang"), self.ga("Flamethrower"), self.ga("HelpingHand")], "fire", "water", "grass"),
		60	: Card("Arcanine", 90, 90, [self.ga("Roar"), self.ga("ThunderFang"), self.ga("Flamethrower"), self.ga("HelpingHand")], "fire", "water", "grass"),



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