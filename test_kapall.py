import unittest
from Player import *
from Presets import *
from InvDeck import *
from Inventory import *

#--------------------------------------------------------------------
# Testing the player class
#--------------------------------------------------------------------
class TestPlayer(unittest.TestCase):
	# Checks if playerAttack returns boolean
	def test_playerAttack(self):
		arni = Player("Arni")
		villi = Player("Villi")
		pre = Presets()
		arni.mainCard = pre.gc("Charizard")
		villi.mainCard = pre.gc("Bulbasaur")
		self.assertTrue(isinstance(arni.attack(2, villi), bool))

	# checks if str method for player is correct
	def test_playerStr(self):
		bla = Player("BlaBlaAlb")
		self.assertEqual(str(bla), "BlaBlaAlb")

	# Checks if isAi method is correct
	def test_playerIsAI(self):
		tilraunardyr = Player("computer")
		tilraunardyr2 = Player("arni")
		self.assertTrue(tilraunardyr.isAI())
		self.assertFalse(tilraunardyr2.isAI())


suite = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
unittest.TextTestRunner(verbosity=2).run(suite)

# -----------------------------------------------------------------------
# Testing the deck class
# -----------------------------------------------------------------------
class TestDeck(unittest.TestCase):

	# Checks if shuffle changes a list.
	def test_deckShuffle(self):
		deck = Deck()
		deck.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		deck.shuffle()
		self.assertFalse(deck.cards == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

	# Tests if the draw method is drawing the correct card
	def test_deckDraw(self):
		deck = Deck()
		deck.cards = [1,2,3,4,5,2,6,54,4,2]
		self.assertEqual(deck.draw(), 2)

	# Checking if the remove method returns the correct value and 
	# checking if it removes the item from the list. Checks also what 
	# happens if you put a negative index as an argument.
	def test_deckRemove(self):
		deck = Deck()
		deck.cards = [0,1,2,3,4,5,6,7,8,9]
		i = 0
		self.assertEqual(deck.remove(0), i)
		i += 1
		# To check if a card was acctually removed
		self.assertEqual(deck.remove(0), i)
		with self.assertRaises(IndexError):
			# Index = -100 not valid
			deck.remove(-100)
			
	def test_deckgetIndexOf(self):
		deck = Deck()
		pre = Presets()
		deck.cards = [pre.gc("Bulbasaur")]
		self.assertEqual(deck.getIndexOf("Bulbasaur"), 0)
		self.assertEqual(deck.getIndexOf("Gamli"), -1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestDeck)
unittest.TextTestRunner(verbosity=2).run(suite)

#----------------------------------------------------------------------
# Testing the Card class
#----------------------------------------------------------------------
class TestCard(unittest.TestCase):
	# Checks if if isdead is returning the correct value
	def test_CardisDead(self):
		card = Card('arni', -15, 100, ["bla","attack"], "grass", "fire", "water")
		self.assertTrue(card.isDead())
		card2 = Card('arni', 14, 100, ["bla","attack"], "grass", "fire", "water")
		self.assertTrue(not card2.isDead())

	def test_Cardattack(self):
		pre = Presets()
		card = pre.gc("Bulbasaur")
		card2 = pre.gc("Charizard")
		# Attack should succeed
		self.assertTrue(card.attack(card.attacks[0], card2))
		card.stamina = 0
		# Attack shuld fail
		self.assertTrue(not card.attack(card.attacks[0], card2))

	# Testing if the use method works correctly
	def test_Carduse(self):
		pre = Presets()
		card = pre.gic("Ether")
		pokemon = pre.gc("Bulbasaur")
		self.assertTrue(pokemon.use(card))

	# Testing if the hasHeal method is working correctly
	def test_CardHasHeal(self):
		pre = Presets()
		canHeal = pre.gc("Slowbro")
		cantHeal = pre.gc("Charmander")
		self.assertTrue(canHeal.hasHeal())
		self.assertFalse(cantHeal.hasHeal())


	# Testing if the needsheal method is working correctly
	def test_CardNeedsHeal(self):
		pre = Presets()
		pika = pre.gc("Pikachu")
		self.assertFalse(pika.needsHeal())
		pika.health = 1
		self.assertTrue(pika.needsHeal())

	# Testing method findHeal for Card
	def test_CardFindHeal(self):
		pre = Presets()
		numberShouldBe = 0
		canHeal = pre.gc("Slowbro")
		self.assertEqual(canHeal.findHeal(), numberShouldBe)

	# Testing method hasStun
	def test_CardHasStun(self):
		pre = Presets()
		canStun = pre.gc("Gengar")
		cantStun = pre.gc("Bulbasaur")
		self.assertTrue(canStun.hasStun())
		self.assertFalse(cantStun.hasStun())

	# Testing method findStun
	def test_CardFindStun(self):
		numberShouldBe = 0
		pre = Presets()
		canStun = pre.gc("Gengar")
		self.assertEqual(canStun.findStun(), numberShouldBe)


suite = unittest.TestLoader().loadTestsFromTestCase(TestCard)
unittest.TextTestRunner(verbosity=2).run(suite)

#----------------------------------------------------------------------
# Testing the Presets class
#----------------------------------------------------------------------
class TestPresets(unittest.TestCase):
	# Checks if gc is working correctly
	def test_Presetsgc(self):
		pre = Presets()
		self.assertEqual(str(pre.gc("Pikachu")), "Pikachu")
		self.assertEqual(str(pre.gc(4)), "Charmander")
		
		
	# Checks if ga is working correctly
	def test_Presetsga(self):
		pre = Presets()
		self.assertEqual(str(pre.ga("MudBomb")), "MudBomb")
		self.assertEqual(str(pre.ga(517)), "Inferno")

suite = unittest.TestLoader().loadTestsFromTestCase(TestCard)
unittest.TextTestRunner(verbosity=2).run(suite)

# -----------------------------------------------------------------------
# Testing the hand class
# -----------------------------------------------------------------------
class TestHand(unittest.TestCase):

	# Checking if the remove method returns the correct value and 
	# checking if it removes the item from the list. Checks also what 
	# happens if you put a negative index as an argument.
	def test_handRemove(self):
		hand = Hand()
		hand.cards = [0,1,2,3]
		i = 0
		self.assertEqual(hand.remove(0), i)
		i += 1
		# To check if a card was acctually removed
		self.assertEqual(hand.remove(0), i)
		with self.assertRaises(IndexError):
			# Index = -100 not valid
			hand.remove(-100)

	# Testing the isFull method
	def test_handisFull(self):
		hand = Hand()
		hand2 = Hand()
		hand.cards = [1,2,3,4,5,6]
		hand2.cards = [1,2,3]
		self.assertTrue(hand.isFull())
		self.assertFalse(hand2.isFull())

	def test_handgetIndexOf(self):
		hand = Hand()
		pre = Presets()
		hand.cards = [pre.gc("Bulbasaur")]
		self.assertEqual(hand.getIndexOf("Bulbasaur"), 0)
		self.assertEqual(hand.getIndexOf("Hundur"), -1)

	def test_handgetNameOfType(self):
		hand = Hand()
		pre = Presets()
		# Bulbasaur is of type "grass" and Charicard of type "fire"
		hand.cards = [pre.gc("Bulbasaur"), pre.gc("Charizard")]
		self.assertEqual(hand.getNameOfType("grass"), "Bulbasaur")
		self.assertEqual(hand.getNameOfType("fire"), "Charizard")
		# No one in hand is of type "water" so the method should return "none"
		self.assertEqual(hand.getNameOfType("water"), "none")

suite = unittest.TestLoader().loadTestsFromTestCase(TestHand)
unittest.TextTestRunner(verbosity=2).run(suite)

# -----------------------------------------------------------------------
# Testing the InvDeck class
# -----------------------------------------------------------------------
class TestinvDeck(unittest.TestCase):

	# Checks if shuffle changes a list.
	def test_invDeckShuffle(self):
		invDeck = InvDeck()
		invDeck.invCards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		invDeck.shuffle()
		self.assertFalse(invDeck.invCards == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

	# Tests if the draw method is drawing the correct card
	def test_invDeckDraw(self):
		invDeck = InvDeck()
		invDeck.invCards = [1,2,3,4,5,2,6,54,4,2]
		self.assertEqual(invDeck.draw(), 2)

	# Checking if the remove method returns the correct value and 
	# checking if it removes the item from the list. Checks also what 
	# happens if you put a negative index as an argument.
	def test_invDeckRemove(self):
		invDeck = InvDeck()
		invDeck.invCards = [0,1,2,3,4,5,6,7,8,9]
		i = 0
		self.assertEqual(invDeck.remove(0), i)
		i += 1
		# To check if a card was acctually removed
		self.assertEqual(invDeck.remove(0), i)
		with self.assertRaises(IndexError):
			# Index = -100 not valid
			invDeck.remove(-100)
			
	def test_invDeckgetIndexOf(self):
		invDeck = InvDeck()
		pre = Presets()
		invDeck.invCards = [pre.gic("Ether")]
		self.assertEqual(invDeck.getIndexOf("Ether"), 0)
		self.assertEqual(invDeck.getIndexOf("Gamli"), -1)

suite = unittest.TestLoader().loadTestsFromTestCase(TestinvDeck)
unittest.TextTestRunner(verbosity=2).run(suite)

# -----------------------------------------------------------------------
# Testing the inventory class
# -----------------------------------------------------------------------
class Testinventory(unittest.TestCase):

	# Checking if the remove method returns the correct value and 
	# checking if it removes the item from the list. Checks also what 
	# happens if you put a negative index as an argument.
	def test_inventoryRemove(self):
		inventory = Inventory()
		inventory.invCards = [0,1,2,3]
		i = 0
		self.assertEqual(inventory.remove(0), i)
		i += 1
		# To check if a card was acctually removed
		self.assertEqual(inventory.remove(0), i)
		with self.assertRaises(IndexError):
			# Index = -100 not valid
			inventory.remove(-100)

	# Testing the isFull method
	def test_inventoryisFull(self):
		inventory = Inventory()
		inventory2 = Inventory()
		inventory.invCards = [1,2,3]
		inventory2.invCards = [1,2]
		self.assertTrue(inventory.isFull())
		self.assertFalse(inventory2.isFull())

	# Testing the getIndexOf method
	def test_inventorygetIndexOf(self):
		inventory = Inventory()
		pre = Presets()
		inventory.invCards = [pre.gic("Ether")]
		# healtpotion2 is in the inventory number zero
		self.assertEqual(inventory.getIndexOf("Ether"), 0)
		# hundur is not in the inventory
		self.assertEqual(inventory.getIndexOf("Hundur"), -1)

suite = unittest.TestLoader().loadTestsFromTestCase(Testinventory)
unittest.TextTestRunner(verbosity=2).run(suite)
