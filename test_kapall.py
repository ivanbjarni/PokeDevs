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

'''
class TestAttack(unittest.TestCase):
	def test_validateStringToNumber(self):
		self.assertTrue(not validateStringToNumber("asd"))
	def test_higher(self):
		self.assertTrue(higher("blabla") == "villa")

suite = unittest.TestLoader().loadTestsFromTestCase(TestFoll)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestHand(unittest.TestCase):
	def test_validateStringToNumber(self):
		self.assertTrue(not validateStringToNumber("asd"))
	def test_higher(self):
		self.assertTrue(higher("blabla") == "villa")

suite = unittest.TestLoader().loadTestsFromTestCase(TestFoll)
unittest.TextTestRunner(verbosity=2).run(suite)
'''