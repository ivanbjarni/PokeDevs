from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *
from util import *
from Presets import *

presets = Presets()

Charmander = presets.gc("Eevee")
Pikachu = presets.gc("Pikachu")



def main():
	print "In the blue corner, weighing 153 pounds, the one, the only Chaaarmander"
	print Charmander.name
	print Charmander.health
	print Charmander.stamina
	for atk in Charmander.attacks:
		print " -"+atk.info()
	print Charmander.poketype
	print Charmander.weakness
	print Charmander.resistance
	print "\nAnd his challenger, our furry electric ball. You might know him as vagina.."
	print "PPPIIIKKAACCHHUU"
	print Pikachu.name
	print Pikachu.health
	print Pikachu.stamina
	for atk in Pikachu.attacks:
		print " -"+str(atk)
	print Pikachu.poketype
	print Pikachu.weakness
	print Pikachu.resistance
	print "\nPlayer 1, your pokemon is Pikachu"
	print "Player 2, your pokemon is Charmander"
	print "But choose wisely..."
	print "I like googling myself... but don't tell anyone"
	print "I also like whiskey 8)"

	




if __name__ == "__main__":
    main()
