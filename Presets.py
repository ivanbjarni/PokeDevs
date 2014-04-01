from Deck import *
from Hand import *
from Card import *
from util import *
from InvCard import *
import random
import copy

class Presets(object):
	invDecks	= []		#invDecks 	Predefined InvDecks of Invcards to be used
	invCards	= []		#
	decks		= []		#Decks		Predefined decks of cards to be used
	cards		= []		#Cards		Predefined cards to be used, Dictionary where key is the pokemon's entry in the national pokedex
	attacks 	= []		#Attacks 	Predefined attacks to be used, Dictionary where key is the official move id


	def __init__(self):
		self.initInvCards()
		self.initAttacks()
		self.initCards()
		self.initDecks()

	def __str__(self):
		return "presets"

	def initInvCards(self):
		self.invCards = {
		0	: InvCard("Ether", 0, 15, False, 1,1,0,0,0),
		1	: InvCard("Elixir", 0, 35, False, 1,1,0,0,0),
		2	: InvCard("MaxEther", 0, 55, False, 1,1,0,0,0),
		3	: InvCard("MaxElixir", 0, 75, False, 1,1,0,0,0),
		4	: InvCard("Potion", 10, 5, False, 1,1,0,0,0),
		5	: InvCard("SuperPotion", 25, 0, False, 1,1,0,0,0),
		6	: InvCard("HyperPotion", 40, 0, False, 1,1,0,0,0),
		7	: InvCard("MaxPotion", 65, 0, False, 1,1,0,0,0),
		9	: InvCard("XSpeed", 0, 0, False, 1.2,1,0,0,0),
		10	: InvCard("XAccuracy", 0, 0, False, 1.4,1,0,0,0),
		11	: InvCard("DireHit", 0, 0, False, 1.6,1,0,0,0),
		12	: InvCard("XAttack", 0, 0, False, 1.8,1,0,0,0),
		13	: InvCard("XSpecial", 0, 0, False, 2,1,0,0,0),
		14	: InvCard("UnStunSpray", 0, 0, True, 1,1,0,0,0),
		15	: InvCard("FullHeal", 20, 0, True, 1,1,0,0,0),
		16	: InvCard("LavaCookie", 0, 25, True, 1,1,0,0,0),
		17	: InvCard("FullRestore", 20, 20, True, 1,1,0,0,0),
		18	: InvCard("XDefense", 0, 0, False, 1,0.75,0,0,0),
		19	: InvCard("GuardSpec", 0, 0, False, 1,0.5,0,0,0),
		20	: InvCard("LifeOrb", -15, 0, False, 2.1,1,0,0,0),
		21	: InvCard("ExpertBelt", 0, 0, False, 1, 1,0.8,0,0),
		22	: InvCard("ZoomLens", 0, 0, False, 1, 1,0,0.05,0),
		23	: InvCard("ScopeLens", 0, 0, False, 1, 1,0,0,0.05),
		}

	def initAttacks(self):
		self.attacks ={
		0	: Attack("Empty", 0, 0, 0, 0, "normal"),				
		2	: Attack("KarateChop", 25, 15, 0, 0, "ground"),				
		3	: Attack("DoubleSlap", 20, 30, 0, 0, "normal"),				
		5	: Attack("MegaPunch", 20, 30, 0, 0, "normal"),				
		10	: Attack("Scratch", 10, 5, 0, 0, "normal"),			
		16	: Attack("Gust", 10, 5, 0, 0, "normal"),			
		17	: Attack("WingAttack", 15, 20, 0, 1, "normal"),	
		21	: Attack("Slam", 18, 25, 0, 0, "normal"),			
		22	: Attack("VineWhip", 7, 5, 0, 0, "grass"),				
		30	: Attack("HornAttack", 15, 30, 0, 1, "normal"),				
		31	: Attack("FuryAttack", 15, 25, 0, 1, "normal"),				
		32	: Attack("HornDrill", 25, 50, 0, 1, "normal"),				
		33	: Attack("Tackle", 7, 5, 0, 0, "normal"),				
		34	: Attack("BodySlam", 18, 24, 0, 0, "normal"),				
		36	: Attack("TakeDown", 10, 5, 0, 0, "normal"),			
		37	: Attack("Thrash", 50, 90, 0, 0, "normal"),			
		38	: Attack("DoubleEdge", 17, 12, 0, 0, "normal"),			
		39	: Attack("TailWhip", 10, 20, 0, 1, "normal"),			
		40	: Attack("PoisonSting", 15, 20, 0, 1, "grass"),			
		41	: Attack("Twineedle", 13, 10, 0, 0, "grass"),
		43	: Attack("Leer", 17, 20, 0, 0, "normal"),			
		44	: Attack("Bite", 15, 15, 0, 0, "normal"),				
		45	: Attack("Growl", 5, 3, 0, 0, "normal"),				
		46	: Attack("Roar", 7, 3, 0, 0, "normal"),				
		47	: Attack("Sing", 0, 25, 0, 2, "normal"),				
		48	: Attack("Supersonic", 5, 35, 0, 2, "normal"),				
		51	: Attack("Acid", 10, 37, 0, 2, "grass"),				
		52	: Attack("Ember", 10, 5, 0, 0, "fire"),			
		53	: Attack("Flamethrower", 16, 25, 0, 0, "fire"),			
		55	: Attack("WaterGun", 18, 14, 0, 0, "water"),			
		56	: Attack("HydroPump", 50, 65, 0, 0, "water"),			
		58	: Attack("IceBeam", 40, 60, 0, 0, "water"),			
		59	: Attack("Blizzard", 40, 50, 25, 0, "water"),			
		60	: Attack("Psybeam", 20, 30, 0, 0, "psychic"),			
		61	: Attack("BubbleBeam", 28, 30, 0, 0, "water"),			
		62	: Attack("AuroraBeam", 28, 30, 0, 0, "water"),			
		63	: Attack("HyperBeam", 58, 65, 12, 0, "normal"),			
		64	: Attack("Peck", 12, 10, 0, 0, "normal"),			
		65	: Attack("DrillPeck", 32, 70, 0, 1, "normal"),			
		66	: Attack("Submission", 28, 6, 7, 0, "ground"),			
		67	: Attack("LowKick", 15, 8, 0, 0, "ground"),			
		71	: Attack("Absorb", 15, 10, -15, 0, "grass"),			
		72	: Attack("MegaDrain", 22, 15, -22, 0, "grass"),			
		74	: Attack("Growth", 0, -10, -7, 0, "normal"),			
		75	: Attack("RazorLeaf", 18, 20, 0, 0, "grass"),			
		76	: Attack("SolarBeam", 47, 35, 10, 0, "grass"),			
		78	: Attack("StunSpore", 0, 68, 0, 3, "grass"),			
		79	: Attack("SleepPowder", 0, 20, 0, 1, "grass"),			
		80	: Attack("PetalDance", 15, 20, 0, 0, "grass"),			
		81	: Attack("StringShot", 10, 14, 0, 1, "grass"),			
		83	: Attack("FireSpin", 20, 25, 0, 0, "fire"),				
		84	: Attack("ThunderShock", 18, 20, 0, 0, "electric"),				
		85	: Attack("Thunderbolt", 30, 50, 0, 0, "electric"),				
		89	: Attack("Earthquake", 50, 80, 0, 0, "ground"),				
		90	: Attack("Fissure", 40, 90, 0, 1, "ground"),				
		91	: Attack("Dig", 0, -20, -20, 1, "ground"),							
		93	: Attack("Confusion", 12, 30, 0, 1, "psychic"),							
		94	: Attack("Hypnosis", 0, 34, 0, 2, "psychic"),				
		95	: Attack("Psychic", 40, 20, 0, 0, "psychic"),				
		96	: Attack("Meditate", 0, 17, -20, 0, "psychic"),				
		98	: Attack("QuickAttack", 12, 10, 0, 0, "normal"),	
		99	: Attack("Rage", 0, 10, -20, 2, "normal"),	
		105	: Attack("Recover", 0, 20, -30, 0, "normal"),	
		106	: Attack("Harden", 0, 20, -18, 0, "normal"),	
		107	: Attack("Minimize", 0, 20, -30, 0, "normal"),	
		108	: Attack("Smokescreen", 0, -10, -20, 0, "normal"),	
		110 : Attack("Withdraw", 0, -18, 10, 0, "normal"),			
		112 : Attack("Barrier", 0, 13, -10, 0, "psychic"),			
		113 : Attack("LightScreen", -5, -10, -10, 1, "normal"),			
		114 : Attack("Haze", 0, -18, 12, 0, "water"),			
		116 : Attack("FocusEnergy", 0, -27, 0, 0, "normal"),	
		118 : Attack("Metronome", 0, 0, 0, 0, "normal"),	
		119 : Attack("MirrorMove", 0, -5, -18, 0, "normal"),	
		120 : Attack("SelfDestruct", 80, 40, 65, 0, "ground"),	
		122 : Attack("Lick", 10, 10, 0, 1, "psychic"),	
		123 : Attack("Smog", 10, 27, 0, 1, "grass"),	
		124 : Attack("Sludge", 18, 30, 0, 0, "grass"),	
		125 : Attack("BoneClub", 30, 0, 15, 0, "normal"),	
		126 : Attack("FireBlast", 18, 30, 0, 1, "fire"),	
		127 : Attack("Waterfall", 25, 45, 0, 0, "water"),	
		141 : Attack("LeechLife", 15, 20, -15, 0, "grass"),	
		143 : Attack("SkyAttack", 15, 20, 0, 0, "normal"),	
		144 : Attack("Transform", 1, 0, 0, 0, "normal"),	
		145 : Attack("Bubble", 10, 5, 0, 0, "water"),	
		146 : Attack("DizzyPunch", 22, 34, 0, 0, "ground"),	
		150 : Attack("Splash", 7, 8, 0, 0, "water"),	
		152 : Attack("Crabhammer", 35, 50, 10, 0, "water"),	
		155 : Attack("Bonemerang", 20, 30, 0, 0, "ground"),	
		157 : Attack("RockSlide", 17, 20, 0, 0, "ground"),	
		158 : Attack("HyperFang", 17, 20, 0, 0, "water"),	
		161 : Attack("TriAttack", 19, 30, 0, 0, "normal"),	
		163 : Attack("Slash", 20, 30, 0, 0, "normal"),	
		171 : Attack("Nightmare", 30, 50, 0, 1, "psychic"),	
		172 : Attack("FlameWheel", 20, 30, 0, 0, "fire"),	
		173 : Attack("Snore", 0, -35, 0, 0, "normal"),	
		175 : Attack("Flail", 15, 30, 0, 0, "water"),	
		184 : Attack("ScaryFace", 8, 25, 8, 1, "normal"),	
		188 : Attack("SludgeBomb", 25, 30, 0, 0, "grass"),	
		192 : Attack("ZapCannon", 30, 40, 0, 1, "electric"),	
		196 : Attack("IcyWind", 15, 30, 0, 1, "water"),	
		198 : Attack("BoneRush", 35, 55, 5, 0, "ground"),	
		200 : Attack("Outrage", 25, -17, 15, 0, "normal"),	
		201 : Attack("Sandstorm", 40, 40, 0, 0, "ground"),	
		202 : Attack("GigaDrain", 30, 50, -30, 0, "grass"),	
		203 : Attack("Endure", 0, 40, -40, 0, "normal"),	
		207 : Attack("Swagger", 0, -35, 0, 0, "normal"),	
		209 : Attack("Spark", 10, 15, 0, 0, "electric"),	
		210 : Attack("FuryCutter", 14, 25, 0, 1, "grass"),	
		219 : Attack("Safeguard", 0, 25, -25, 1, "normal"),	
		222 : Attack("Magnitude", 18, 30, 0, 1, "ground"),	
		223 : Attack("DynamicPunch", 45, 55, 3, 0, "ground"),	
		224 : Attack("Megahorn", 30, 55, 5, 0, "grass"),	
		229 : Attack("RapidSpin", 7, 18, 0, 1, "normal"),			
		238 : Attack("CrossChop", 33, 50, 0, 1, "ground"),			
		240 : Attack("RainDance", 5, -12, -5, 0, "water"),			
		241 : Attack("SunnyDay", -5, 20, -30, 0, "fire"),			
		246 : Attack("AncientPower", 8, 32, -30, 0, "ground"),			
		247 : Attack("ShadowBall", 5, -23, 0, 0, "psychic"),			
		250 : Attack("Whirlpool", 15, 15, -5, 0, "water"),			
		252 : Attack("FakeOut", 12, 7, 0, 0, "normal"),			
		253 : Attack("Uproar", 30, 40, 0, 0, "normal"),			
		264 : Attack("FocusPunch", 15, 15, 0, 0, "ground"),			
		268 : Attack("Charge", 0, -30, 5, 0, "electric"),			
		270 : Attack("HelpingHand", -30, 18, 0, 2, "normal"),			
		276 : Attack("Superpower", 7, 20, -20, 0, "normal"),			
		279 : Attack("Revenge", 15, 20, 0, 0, "normal"),			
		283 : Attack("Endeavor", 15, 20, -10, 0, "normal"),			
		291 : Attack("Dive", 5, 5, -10, 0, "water"),			
		304 : Attack("HyperVoice", 15, 20, 0, 0, "normal"),			
		305 : Attack("PoisonFang", 20, 30, 0, 1, "grass"),			
		318 : Attack("SilverWind", 20, 10, -10, 0, "grass"),			
		324 : Attack("SignalBeam", 15, 18, 0, 0, "grass"),			
		325 : Attack("ShadowPunch", 8, -10, -5, 0, "psychic"),			
		331 : Attack("BulletSeed", 12, 15, 0, 0, "grass"),			
		332 : Attack("AerialAce", 30, 0, 18, 0, "normal"),			
		346 : Attack("WaterSport", 12, 10, -25, 0, "normal"),			
		349 : Attack("DragonDance", 0, 20, -30, 0, "normal"),			
		350 : Attack("RockBlast", 20, 18, 0, 0, "ground"),			
		352 : Attack("WaterPulse", 28, 30, 0, 0, "water"),			
		361 : Attack("HealingWish", -5, 5, -20, 0, "normal"),			
		362 : Attack("Brine", 15, 8, 0, 0, "water"),			
		364 : Attack("Feint", 0, -20, 10, 0, "normal"),			
		370 : Attack("CloseCombat", 30, 40, 0, 0, "ground"),			
		382 : Attack("MeFirst", 0, 30, 0, 2, "normal"),			
		390 : Attack("ToxicSpikes", 15, 28, 0, 1, "grass"),			
		394 : Attack("FlareBlitz", 30, 40, 0, 1, "fire"),				
		401 : Attack("AquaTail", 15, 25, 0, 0, "water"),				
		402 : Attack("SeedBomb", 25, 40, 0, 0, "grass"),				
		403 : Attack("AirSlash", 25, 35, 0, 0, "normal"),				
		404 : Attack("X-Scissor", 30, 40, 0, 0, "grass"),				
		405 : Attack("BugBuzz", 35, 40, 0, 0, "grass"),				
		414 : Attack("EarthPower", 40, 55, 0, 1, "ground"),				
		416 : Attack("GigaImpact", 40, 65, 0, 1, "normal"),				
		422 : Attack("ThunderFang", 15, 16, 0, 0, "electric"),				
		424 : Attack("FireFang", 15, 26, 0, 1, "fire"),				
		426 : Attack("MudBomb", 20, 20, 0, 0, "normal"),				
		427 : Attack("PsychoCut", 22, 30, 0, 0, "psychic"),				
		428 : Attack("ZenHeadbutt", 10, -20, 0, 0, "psychic"),				
		435 : Attack("Discharge", 0, 55, -55, 0, "electric"),				
		436 : Attack("LavaPlume", 25, 35, -10, 0, "fire"),				
		437 : Attack("LeafStorm", 35, 50, 0, 0, "grass"),				
		441 : Attack("GunkShot", 20, 40, 0, 1, "grass"),				
		443 : Attack("MagnetBomb", 50, 20, 35, 2, "electric"),				
		445 : Attack("Captivate", 30, 40, 0, 0, "normal"),				
		450 : Attack("BugBite", 15, 7, 0, 0, "grass"),				
		451 : Attack("ChargeBeam", 25, 5, 10, 0, "electric"),				
		452 : Attack("WoodHammer", 25, 50, 0, 1, "grass"),				
		453 : Attack("AquaJet", 25, 50, 0, 1, "water"),				
		472 : Attack("WonderRoom", 5, 32, -10, 1, "psychic"),				
		473 : Attack("Psyshock", 30, 15, 0, 0, "psychic"),				
		486	: Attack("Thunder", 30, 30, 10, 0, "electric"),			
		487	: Attack("Soak", 5, 35, 0, 1, "water"),			
		490	: Attack("LowSweep", 15, 10, 0, 0, "ground"),			
		491	: Attack("AcidSpray", 25, 40, 0, 0, "grass"),			
		495	: Attack("AfterYou", 0, 0, 0, 0, "normal"),			
		498	: Attack("ChipAway", 30, 45, 0, 0, "normal"),			
		505	: Attack("HealPulse", 0, 10, -25, 0, "psychic"),			
		506	: Attack("Hex", 15, 35, -25, 1, "psychic"),			
		512	: Attack("Acrobatics", 18, 15, 0, 0, "normal"),			
		515	: Attack("FinalGambit", 40, 0, 25, 0, "normal"),			
		517	: Attack("Inferno", 40, 40, 0, 0, "fire"),				
		531	: Attack("HeartStamp", 25, 40, 0, 0, "psychic"),				
		540	: Attack("Psystrike", 15, 30, 0, 1, "psychic"),				
		542	: Attack("Hurricane", 25, 50, 0, 1, "normal"),				
		562	: Attack("Belch", 35, 50, 0, 1, "grass"),				
		565	: Attack("FellStinger", 30, 30, 10, 0, "grass"),				
		572	: Attack("PetalBlizzard", 35, 50, 0, 0, "grass"),
		577	: Attack("DrainingKiss", 15, 10, -15, 0, "psychic"),
		580	: Attack("GrassyTerrain", 0, 40, -30, 0, "grass"),
		583	: Attack("PlayRough", 27, 45, 0, 0, "normal"),
		585	: Attack("Moonblast", 25, 45, 0, 0, "normal"),
		678	: Attack("ElectroBall", 18, 20, -12, 0, "electric")
		

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
		11	: Card("Metapod", 50, 85, [self.ga("Tackle"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Harden")], "grass", "ground", "grass"),
		12	: Card("Butterfree", 60, 110, [self.ga("Gust"), self.ga("Supersonic"), self.ga("SilverWind"), self.ga("BugBuzz")], "grass", "fire", "grass"),
		13	: Card("Weedle", 40, 60, [self.ga("PoisonSting"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Empty")], "grass", "ground", "grass"),
		14	: Card("Kakuna", 45, 85, [self.ga("PoisonSting"), self.ga("StringShot"), self.ga("BugBite"), self.ga("Harden")], "grass", "fire", "grass"),
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
		42	: Card("Golbat", 75, 90, [self.ga("LeechLife"), self.ga("Acrobatics"), self.ga("PoisonFang"), self.ga("AirSlash")], "normal", "electric", "ground"),
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
		60	: Card("Poliwag", 40, 90, [self.ga("WaterSport"), self.ga("RainDance"), self.ga("Hypnosis"), self.ga("WaterGun")], "water", "grass", "water"),
		61	: Card("Poliwhirl", 65, 110, [self.ga("WaterSport"), self.ga("RainDance"), self.ga("Hypnosis"), self.ga("WaterGun")], "water", "grass", "water"),
		62	: Card("Poliwrath", 90, 100, [self.ga("DoubleSlap"), self.ga("RainDance"), self.ga("Hypnosis"), self.ga("WaterGun")], "water", "grass", "water"),
		63	: Card("Abra", 25, 70, [self.ga("Psyshock"), self.ga("RainDance"), self.ga("Hypnosis"), self.ga("LightScreen")], "psychic", "fire", "psychic"),
		64	: Card("Kadabra", 40, 100, [self.ga("Psychic"), self.ga("Recover"), self.ga("Hypnosis"), self.ga("LightScreen")], "psychic", "fire", "psychic"),
		65	: Card("Alakazam", 55, 130, [self.ga("Psychic"), self.ga("Recover"), self.ga("HyperBeam"), self.ga("LightScreen")], "psychic", "fire", "psychic"),
		66	: Card("Machop", 70, 70, [self.ga("LowKick"), self.ga("FocusEnergy"), self.ga("Submission"), self.ga("LowSweep")], "ground", "psychic", "ground"),
		67	: Card("Machoke", 80, 80, [self.ga("LowKick"), self.ga("FocusEnergy"), self.ga("Submission"), self.ga("DynamicPunch")], "ground", "psychic", "ground"),
		68	: Card("Machamp", 90, 90, [self.ga("KarateChop"), self.ga("FocusEnergy"), self.ga("Submission"), self.ga("DynamicPunch")], "ground", "psychic", "ground"),
		69	: Card("Bellsprout", 50, 100, [self.ga("RazorLeaf"), self.ga("VineWhip"), self.ga("Acid"), self.ga("Growth")], "grass", "fire", "grass"),
		70	: Card("Weepinbell", 65, 95, [self.ga("Slam"), self.ga("RazorLeaf"), self.ga("Acid"), self.ga("StunSpore")], "grass", "fire", "grass"),
		71	: Card("Victreebell", 80, 90, [self.ga("Slam"), self.ga("VineWhip"), self.ga("Acid"), self.ga("RazorLeaf")], "grass", "fire", "grass"),
		72	: Card("Tentacool", 40, 80, [self.ga("PoisonSting"), self.ga("Acid"), self.ga("BubbleBeam"), self.ga("AcidSpray")], "water", "psychic", "fire"),
		73	: Card("Tentacruel", 80, 95, [self.ga("PoisonSting"), self.ga("BubbleBeam"), self.ga("HydroPump"), self.ga("Acid")], "water", "psychic", "fire"),
		74	: Card("Geodude", 40, 95, [self.ga("Tackle"), self.ga("SelfDestruct"), self.ga("DoubleEdge"), self.ga("Magnitude")], "ground", "water", "electric"),
		75	: Card("Graveler", 55, 95, [self.ga("Tackle"), self.ga("SelfDestruct"), self.ga("Earthquake"), self.ga("Magnitude")], "ground", "water", "electric"),
		76	: Card("Golem", 55, 95, [self.ga("Tackle"), self.ga("SelfDestruct"), self.ga("Earthquake"), self.ga("Magnitude")], "ground", "water", "electric"),
		77	: Card("Ponyta", 50, 85, [self.ga("Tackle"), self.ga("Ember"), self.ga("FireSpin"), self.ga("FireBlast")], "fire", "ground", "grass"),
		78	: Card("Rapidash", 65, 100, [self.ga("Ember"), self.ga("Inferno"), self.ga("FlareBlitz"), self.ga("FireBlast")], "fire", "ground", "grass"),
		79	: Card("Slowpoke", 90, 80, [self.ga("Growl"), self.ga("WaterPulse"), self.ga("Confusion"), self.ga("HealPulse")], "psychic", "grass", "water"),
		80	: Card("Slowbro", 95, 95, [self.ga("HealPulse"), self.ga("WaterGun"), self.ga("ZenHeadbutt"), self.ga("Confusion")], "psychic", "grass", "water"),
		81	: Card("Magnemite", 25, 60, [self.ga("Tackle"), self.ga("ThunderShock"), self.ga("Spark"), self.ga("ZapCannon")], "electric", "ground", "grass"),
		82	: Card("Magneton", 50, 80, [self.ga("ZapCannon"), self.ga("ThunderShock"), self.ga("MagnetBomb"), self.ga("ElectroBall")], "electric", "ground", "grass"),
		83	: Card("Farfetch'd", 52, 80, [self.ga("Peck"), self.ga("FuryAttack"), self.ga("AerialAce"), self.ga("Feint")], "normal", "electric", "grass"),
		84	: Card("Doduo", 35, 150, [self.ga("Peck"), self.ga("FuryAttack"), self.ga("Uproar"), self.ga("Rage")], "normal", "electric", "grass"),
		85	: Card("Dodrio", 60, 150, [self.ga("Peck"), self.ga("FuryAttack"), self.ga("Rage"), self.ga("Thrash")], "normal", "electric", "grass"),
		86	: Card("Seel", 65, 75, [self.ga("Growl"), self.ga("AquaJet"), self.ga("Dive"), self.ga("AquaTail")], "water", "electric", "fire"),
		87	: Card("Dewgong", 90, 85, [self.ga("IcyWind"), self.ga("AquaJet"), self.ga("IceBeam"), self.ga("AquaTail")], "water", "electric", "fire"),
		88	: Card("Grimer", 80, 85, [self.ga("Harden"), self.ga("MudBomb"), self.ga("Sludge"), self.ga("GunkShot")], "grass", "psychic", "grass"),
		89	: Card("Muk", 105, 100, [self.ga("Harden"), self.ga("Belch"), self.ga("SludgeBomb"), self.ga("GunkShot")], "grass", "psychic", "grass"),
		90	: Card("Shellder", 30, 80, [self.ga("Tackle"), self.ga("Withdraw"), self.ga("Whirlpool"), self.ga("HydroPump")], "water", "grass", "fire"),
		91	: Card("Cloyster", 50, 100, [self.ga("HydroPump"), self.ga("Withdraw"), self.ga("AuroraBeam"), self.ga("ToxicSpikes")], "water", "grass", "fire"),
		92	: Card("Gastly", 30, 70, [self.ga("Lick"), self.ga("Hypnosis"), self.ga("ShadowBall"), self.ga("Hex")], "psychic", "psychic", "ground"),
		93	: Card("Haunter", 45, 80, [self.ga("Lick"), self.ga("Nightmare"), self.ga("ShadowBall"), self.ga("Hex")], "psychic", "psychic", "ground"),
		94	: Card("Gengar", 60, 95, [self.ga("Lick"), self.ga("Nightmare"), self.ga("ShadowPunch"), self.ga("Hex")], "psychic", "psychic", "ground"),
		95	: Card("Onix", 35, 90, [self.ga("Harden"), self.ga("Dig"), self.ga("DoubleEdge"), self.ga("Sandstorm")], "ground", "water", "electric"),
		96	: Card("Drowzee", 60, 80, [self.ga("Confusion"), self.ga("Psybeam"), self.ga("ZenHeadbutt"), self.ga("Meditate")], "psychic", "grass", "ground"),
		97	: Card("Hypno", 85, 100, [self.ga("Hypnosis"), self.ga("Psyshock"), self.ga("ZenHeadbutt"), self.ga("Meditate")], "psychic", "grass", "ground"),
		98	: Card("Krabby", 30, 80, [self.ga("Bubble"), self.ga("BubbleBeam"), self.ga("Harden"), self.ga("Crabhammer")], "water", "electric", "water"),
		99	: Card("Kingler", 55, 100, [self.ga("Brine"), self.ga("BubbleBeam"), self.ga("Harden"), self.ga("Crabhammer")], "water", "electric", "water"),
		100	: Card("Voltorb", 40, 80, [self.ga("Tackle"), self.ga("Spark"), self.ga("ChargeBeam"), self.ga("ElectroBall")], "electric", "ground", "electric"),
		101	: Card("Electrode", 60, 110, [self.ga("Spark"), self.ga("ElectroBall"), self.ga("Charge"), self.ga("SelfDestruct")], "electric", "ground", "electric"),
		102	: Card("Exeggcute", 60, 70, [self.ga("BulletSeed"), self.ga("StunSpore"), self.ga("Confusion"), self.ga("SolarBeam")], "grass", "fire", "psychic"),
		103	: Card("Exeggutor", 95, 100, [self.ga("SeedBomb"), self.ga("WoodHammer"), self.ga("Confusion"), self.ga("LeafStorm")], "grass", "fire", "psychic"),
		104	: Card("Cubone", 50, 75, [self.ga("Growl"), self.ga("BoneClub"), self.ga("Bonemerang"), self.ga("DoubleEdge")], "ground", "water", "electric"),
		105	: Card("Marowak", 60, 90, [self.ga("TailWhip"), self.ga("BoneClub"), self.ga("Bonemerang"), self.ga("BoneRush")], "ground", "water", "electric"),
		106	: Card("Hitmonlee", 50, 105, [self.ga("FocusEnergy"), self.ga("Revenge"), self.ga("Endure"), self.ga("CloseCombat")], "ground", "psychic", "ground"),
		107	: Card("Hitmonchan", 50, 105, [self.ga("FocusEnergy"), self.ga("FocusPunch"), self.ga("Endure"), self.ga("CloseCombat")], "ground", "psychic", "ground"),
		108	: Card("Lickitung", 90, 80, [self.ga("Lick"), self.ga("Supersonic"), self.ga("Slam"), self.ga("ChipAway")], "normal", "ground", "psychic"),
		109	: Card("Koffing", 40, 80, [self.ga("Tackle"), self.ga("Smog"), self.ga("Sludge"), self.ga("Haze")], "grass", "psychic", "grass"),
		110	: Card("Weezing", 65, 100, [self.ga("Smog"), self.ga("SludgeBomb"), self.ga("Haze"), self.ga("SelfDestruct")], "grass", "psychic", "grass"),
		111	: Card("Rhyhorn", 80, 80, [self.ga("HornDrill"), self.ga("Earthquake"), self.ga("ScaryFace"), self.ga("TakeDown")], "ground", "grass", "normal"),
		112	: Card("Rhydon", 105, 100, [self.ga("Megahorn"), self.ga("Earthquake"), self.ga("ScaryFace"), self.ga("TakeDown")], "ground", "grass", "normal"),
		113	: Card("Chansey", 250, 120, [self.ga("DoubleSlap"), self.ga("LightScreen"), self.ga("HealingWish"), self.ga("TakeDown")], "normal", "ground", "none"),
		114	: Card("Tangela", 65, 120, [self.ga("MegaDrain"), self.ga("StunSpore"), self.ga("VineWhip"), self.ga("Slam")], "grass", "fire", "water"),
		115	: Card("Kangaskhan", 105, 100, [self.ga("FakeOut"), self.ga("Rage"), self.ga("ChipAway"), self.ga("DizzyPunch")], "normal", "ground", "psychic"),
		116	: Card("Horsea", 30, 75, [self.ga("WaterGun"), self.ga("Bubble"), self.ga("BubbleBeam"), self.ga("Smokescreen")], "water", "grass", "water"),
		117	: Card("Seadra", 55, 90, [self.ga("WaterGun"), self.ga("HydroPump"), self.ga("Brine"), self.ga("Smokescreen")], "water", "grass", "water"),
		118	: Card("Goldeen", 45, 80, [self.ga("Peck"), self.ga("WaterPulse"), self.ga("FuryAttack"), self.ga("Waterfall")], "water", "electric", "fire"),
		119	: Card("Seaking", 80, 90, [self.ga("HornAttack"), self.ga("WaterPulse"), self.ga("Soak"), self.ga("Waterfall")], "water", "electric", "fire"),
		120	: Card("Staryu", 30, 60, [self.ga("WaterGun"), self.ga("BubbleBeam"), self.ga("Brine"), self.ga("HydroPump")], "water", "electric", "fire"),
		121	: Card("Starmie", 60, 85, [self.ga("WaterGun"), self.ga("RapidSpin"), self.ga("Recover"), self.ga("HydroPump")], "water", "electric", "fire"),
		122	: Card("Mr.Mime", 40, 80, [self.ga("Confusion"), self.ga("Psybeam"), self.ga("Barrier"), self.ga("DoubleSlap")], "psychic", "grass", "psychic"),
		123	: Card("Scyther", 70, 120, [self.ga("WingAttack"), self.ga("FuryCutter"), self.ga("X-Scissor"), self.ga("AirSlash")], "grass", "fire", "ground"),
		124	: Card("Jynx", 65, 80, [self.ga("DrainingKiss"), self.ga("HeartStamp"), self.ga("DoubleSlap"), self.ga("Blizzard")], "psychic", "ground", "psychic"),
		125	: Card("Electabuzz", 65, 90, [self.ga("ThunderShock"), self.ga("ElectroBall"), self.ga("Thunderbolt"), self.ga("Discharge")], "electric", "ground", "electric"),
		126	: Card("Magmar", 65, 90, [self.ga("SunnyDay"), self.ga("Smog"), self.ga("FireSpin"), self.ga("FireBlast")], "fire", "ground", "grass"),
		127	: Card("Pinsir", 65, 125, [self.ga("Revenge"), self.ga("Harden"), self.ga("Superpower"), self.ga("X-Scissor")], "grass", "fire", "ground"),
		128	: Card("Tauros", 75, 100, [self.ga("Tackle"), self.ga("Rage"), self.ga("HornAttack"), self.ga("GigaImpact")], "normal", "ground", "psychic"),
		129	: Card("Magikarp", 20, 300, [self.ga("Splash"), self.ga("Tackle"), self.ga("Flail"), self.ga("Empty")], "water", "electric", "water"),
		130	: Card("Gyarados", 95, 120, [self.ga("Leer"), self.ga("AquaTail"), self.ga("HydroPump"), self.ga("HyperBeam")], "water", "electric", "ground"),
		131	: Card("Lapras", 130, 85, [self.ga("Sing"), self.ga("WaterGun"), self.ga("WaterPulse"), self.ga("HydroPump")], "water", "ground", "water"),
		132	: Card("Ditto", 48, 85, [self.ga("Transform"), self.ga("Empty"), self.ga("Empty"), self.ga("Empty")], "normal", "ground", "psychic"),
		133	: Card("Eevee", 55, 100, [self.ga("Tackle"), self.ga("QuickAttack"), self.ga("FocusEnergy"), self.ga("Bite")], "normal", "ground", "psychic"),
		134	: Card("Vaporeon", 130, 90, [self.ga("WaterGun"), self.ga("HelpingHand"), self.ga("WaterPulse"), self.ga("HydroPump")], "water", "electric", "fire"),
		135	: Card("Jolteon", 65, 120, [self.ga("ThunderShock"), self.ga("HelpingHand"), self.ga("ThunderFang"), self.ga("Thunder")], "electric", "ground", "normal"),
		136	: Card("Flareon", 65, 120, [self.ga("Ember"), self.ga("HelpingHand"), self.ga("LavaPlume"), self.ga("FireFang")], "fire", "ground", "grass"),
		137	: Card("Porygon", 65, 85, [self.ga("Tackle"), self.ga("Psybeam"), self.ga("Recover"), self.ga("TriAttack")], "normal", "ground", "psychic"),
		138	: Card("Omanyte", 35, 75, [self.ga("Withdraw"), self.ga("WaterGun"), self.ga("Leer"), self.ga("RockBlast")], "ground", "ground", "normal"),
		139	: Card("Omastar", 70, 90, [self.ga("Withdraw"), self.ga("WaterGun"), self.ga("RockBlast"), self.ga("HydroPump")], "ground", "grass", "normal"),
		140	: Card("Kabuto", 30, 75, [self.ga("RockBlast"), self.ga("Absorb"), self.ga("AquaJet"), self.ga("Harden")], "ground", "ground", "normal"),
		141	: Card("Kabutops", 60, 95, [self.ga("Scratch"), self.ga("Absorb"), self.ga("AquaJet"), self.ga("AncientPower")], "ground", "grass", "normal"),
		142	: Card("Aerodactyl", 80, 100, [self.ga("WingAttack"), self.ga("RockSlide"), self.ga("HyperBeam"), self.ga("AncientPower")], "ground", "electric", "ground"),
		143	: Card("Snorlax", 160, 80, [self.ga("Tackle"), self.ga("ChipAway"), self.ga("GigaImpact"), self.ga("Snore")], "normal", "ground", "psychic"),
		144	: Card("Articuno", 90, 90, [self.ga("IceBeam"), self.ga("Blizzard"), self.ga("Gust"), self.ga("AncientPower")], "water", "grass", "ground"),
		145	: Card("Zapdos", 90, 90, [self.ga("ThunderShock"), self.ga("DrillPeck"), self.ga("Discharge"), self.ga("ZapCannon")], "electric", "water", "ground"),
		146	: Card("Moltres", 90, 100, [self.ga("Ember"), self.ga("Flamethrower"), self.ga("SkyAttack"), self.ga("AncientPower")], "electric", "water", "ground"),
		147	: Card("Dratini", 41, 85, [self.ga("Safeguard"), self.ga("Leer"), self.ga("AquaTail"), self.ga("HyperBeam")], "normal", "psychic", "fire"),
		148	: Card("Dragonair", 61, 95, [self.ga("Outrage"), self.ga("Leer"), self.ga("AquaTail"), self.ga("HyperBeam")], "normal", "psychic", "fire"),
		149	: Card("Dragonite", 91, 110, [self.ga("Outrage"), self.ga("Hurricane"), self.ga("DragonDance"), self.ga("HyperBeam")], "normal", "psychic", "fire"),
		150	: Card("Mewtwo", 106, 150, [self.ga("Recover"), self.ga("PsychoCut"), self.ga("Psystrike"), self.ga("MeFirst")], "psychic", "none", "normal"),
		151	: Card("Mew", 100, 150, [self.ga("Recover"), self.ga("MegaPunch"), self.ga("AncientPower"), self.ga("Psychic")], "psychic", "none", "normal")
		}


	def initDecks(self):
		#Ivan's favorite team
		DreamTeamIvan = Deck()
		DreamTeamIvan.name = "DreamTeamIvan"
		DreamTeamIvan.setCards([self.gc("Sandslash"),self.gc("Pidgeot"),self.gc("Chansey"),self.gc("Lapras"),self.gc("Poliwhirl"),self.gc("Dragonite"),self.gc("Hypno"),self.gc("Tangela"),self.gc("Nidoqueen"),self.gc("Gyarados")])
		
		#The best according to 45 minutes of data collection on the 25/03/14
		TheElite = Deck()
		TheElite.name = "TheElite"
		TheElite.setCards([self.gc("Pidgeot"),self.gc("Sandslash"),self.gc("Hypno"),self.gc("Fearow"),self.gc("Mewtwo"),self.gc("Slowbro"),self.gc("Dragonite"),self.gc("Machamp"),self.gc("Blastoise"),self.gc("Vileplume")])

		#the first 10 of ash's pokemon according to the anime
		TeamAsh = Deck()
		TeamAsh.name = "TeamAsh"
		TeamAsh.setCards([self.gc("Pikachu"),self.gc("Butterfree"),self.gc("Pidgeot"),self.gc("Bulbasaur"),self.gc("Charizard"),self.gc("Squirtle"),self.gc("Kingler"),self.gc("Primeape"),self.gc("Muk"),self.gc("Tauros")])

		#only cute pokemon
		TheCuties = Deck()
		TheCuties.name = "TheCuties"
		TheCuties.setCards([self.gc("Wigglytuff"),self.gc("Eevee"),self.gc("Dewgong"),self.gc("Ninetales"),self.gc("Jigglypuff"),self.gc("Clefairy"),self.gc("Oddish"),self.gc("Ponyta"),self.gc("Vulpix"),self.gc("Chansey")])

		#Only water and fighting pokemon kinda
		FishAndFighters = Deck()
		FishAndFighters.name = "FishAndFighters"
		FishAndFighters.setCards([self.gc("Goldeen"),self.gc("Starmie"),self.gc("Seaking"),self.gc("Shellder"),self.gc("Poliwhirl"),self.gc("Poliwrath"),self.gc("Hitmonlee"),self.gc("Hitmonchan"),self.gc("Machop"),self.gc("Machamp")])

		#The legendairy pokemon
		TheLegends = Deck()
		TheLegends.name = "TheLegends"
		TheLegends.setCards([self.gc("Mew"),self.gc("Mewtwo"),self.gc("Moltres"),self.gc("Zapdos"),self.gc("Articuno"),self.gc("Dragonite"),self.gc("Dragonair"),self.gc("Aerodactyl"),self.gc("Omastar"),self.gc("Kabutops")])

		#only flying types
		SkyTerror = Deck()
		SkyTerror.name = "SkyTerror"
		SkyTerror.setCards([self.gc("Pidgey"),self.gc("Pidgeotto"),self.gc("Pidgeot"),self.gc("Zapdos"),self.gc("Articuno"),self.gc("Moltres"),self.gc("Farfetch'd"),self.gc("Aerodactyl"),self.gc("Spearow"),self.gc("Fearow")])

		#only starter pokemons and their evolved forms
		TheStarters = Deck()
		TheStarters.name = "TheStarters"
		TheStarters.setCards([self.gc("Pikachu"),self.gc("Bulbasaur"),self.gc("Ivysaur"),self.gc("Venusaur"),self.gc("Charmander"),self.gc("Charmeleon"),self.gc("Charizard"),self.gc("Squirtle"),self.gc("Wartortle"),self.gc("Blastoise")])

		#only big pokemons
		TheBigOnes = Deck()
		TheBigOnes.name = "TheBigOnes"
		TheBigOnes.setCards([self.gc("Snorlax"),self.gc("Dragonite"),self.gc("Gyarados"),self.gc("Kangaskhan"),self.gc("Tentacruel"),self.gc("Zapdos"),self.gc("Moltres"),self.gc("Articuno"),self.gc("Kabutops"),self.gc("Lapras")])

		#psychic and fire pokemon
		MindFire = Deck()
		MindFire.name = "MindFire"
		MindFire.setCards([self.gc("Abra"),self.gc("Kadabra"),self.gc("Alakazam"),self.gc("Hypno"),self.gc("Drowzee"),self.gc("Ponyta"),self.gc("Moltres"),self.gc("Rapidash"),self.gc("Charmeleon"),self.gc("Vulpix")])

		#grass and normal pokemon
		MoonGarden = Deck()
		MoonGarden.name = "MoonGarden"
		MoonGarden.setCards([self.gc("Clefairy"),self.gc("Clefable"),self.gc("Chansey"),self.gc("Zubat"),self.gc("Golbat"),self.gc("Paras"),self.gc("Parasect"),self.gc("Oddish"),self.gc("Gloom"),self.gc("Vileplume")])

		#only bug pokemon
		BugParadise = Deck()
		BugParadise.name = "BugParadise"
		BugParadise.setCards([self.gc("Venonat"),self.gc("Venomoth"),self.gc("Caterpie"),self.gc("Metapod"),self.gc("Butterfree"),self.gc("Weedle"),self.gc("Kakuna"),self.gc("Beedrill"),self.gc("Pinsir"),self.gc("Scyther")])

		#Only pink and purple pokemon
		PinkAndPurple = Deck()
		PinkAndPurple.name = "PinkAndPurple"
		PinkAndPurple.setCards([self.gc("Slowpoke"),self.gc("Slowbro"),self.gc("Koffing"),self.gc("Weezing"),self.gc("Gastly"),self.gc("Haunter"),self.gc("Gengar"),self.gc("Grimer"),self.gc("Muk"),self.gc("NidoranM")])

		#thunder and grass pokemon
		ElectricForest = Deck()
		ElectricForest.name = "ElectricForest"
		ElectricForest.setCards([self.gc("Bellsprout"),self.gc("Weepinbell"),self.gc("Victreebell"),self.gc("Exeggcute"),self.gc("Exeggutor"),self.gc("Electabuzz"),self.gc("Jolteon"),self.gc("Pikachu"),self.gc("Raichu"),self.gc("Vileplume")])

		#only pokemon that are made out of rock and metal
		RockAndMetal = Deck()
		RockAndMetal.name = "RockAndMetal"
		RockAndMetal.setCards([self.gc("Porygon"),self.gc("Magnemite"),self.gc("Magneton"),self.gc("Voltorb"),self.gc("Electrode"),self.gc("Rhyhorn"),self.gc("Rhydon"),self.gc("Geodude"),self.gc("Graveler"),self.gc("Golem")])

		self.decks = {
		1 	: TeamAsh,
		2 	: TheCuties,
		3 	: FishAndFighters,
		4 	: TheLegends,
		5 	: SkyTerror,
		6 	: TheStarters,
		7 	: TheBigOnes,
		8 	: MindFire,
		9 	: MoonGarden,
		10 	: BugParadise,
		11 	: PinkAndPurple,
		12 	: ElectricForest,
		13 	: RockAndMetal,
		14 	: TheElite,
		27 	: DreamTeamIvan
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
			return copy.deepcopy(self.cards[card])
		else:
			return self.getCardByName(card)

	def getCardByName(self, string):
		for key, val in self.cards.iteritems():
			if val.name == string:
				return copy.deepcopy(val)
		print "card not found: getCardByName"+string
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
		print "invcard not found: getCardByName"+string
		return -1

	def getRandomAttack(self):
		return random.choice(self.attaks.values())

	def getRandomDeck(self):
		randDeck = Deck()
		for i in xrange(0,10):
			randDeck.add(self.getRandomCard())
		return randDeck

	def getRandomCard(self):
		return copy.deepcopy(random.choice(self.cards.values()))

	def getRandomInvCard(self):
		return copy.deepcopy(random.choice(self.invCards.values()))

	def getTypeOfName(self, string):
		for key, val in self.cards.iteritems():
			if val.name == string:
				return val.type
		print "card not found: getTypeOfName"
		return -1

	#Short for get Deck
	def gd(self, deck):
		if isNumber(deck):
			return copy.deepcopy(self.decks[deck])
		else:
			return self.getDeckByName(deck)

	def getDeckByName(self, string):
		if string == "random":
			return self.getRandomDeck()
		for key, val in self.decks.iteritems():
			if val.name == string:
				return copy.deepcopy(val)
		print "deck not found: getDeckByName"+string
		return -1