import unittest
from Player import *
from Presets import *

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

	def test_playerStr(self):
		bla = Player("BlaBlaAlb")
		self.assertEqual(str(bla), "BlaBlaAlb")

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
	def test_isDead(self):
		card = Card('arni', -15, 100, ["bla","attack"], "grass", "fire", "water")
		self.assertTrue(card.isDead())
		card2 = Card('arni', 14, 100, ["bla","attack"], "grass", "fire", "water")
		self.assertTrue(not card2.isDead())

	def test_attack(self):
		pre = Presets()
		card = pre.gc("Bulbasaur")
		card2 = pre.gc("Charizard")
		# Attack should succeed
		self.assertTrue(card.attack(card.attacks[0], card2))
		card.stamina = 0
		# Attack shuld fail
		self.assertTrue(not card.attack(card.attacks[0], card2))


suite = unittest.TestLoader().loadTestsFromTestCase(TestCard)
unittest.TextTestRunner(verbosity=2).run(suite)

#----------------------------------------------------------------------
# Testing the Presets class
#----------------------------------------------------------------------
class TestPresets(unittest.TestCase):
	# Checks if gc is working correctly
	def test_gc(self):
		pre = Presets()
		self.assertEqual(str(pre.gc("Pikachu")), "Pikachu")
		self.assertEqual(str(pre.gc(4)), "Charmander")
		
		
	# Checks if ga is working correctly
	def test_ga(self):
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

suite = unittest.TestLoader().loadTestsFromTestCase(TestHand)
unittest.TextTestRunner(verbosity=2).run(suite)