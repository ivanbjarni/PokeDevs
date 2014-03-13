from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *

Charmander = Card("Charmander", 39, 39, 90, ["Growl", "FireFang", "Flamethrower", "Inferno"], "fire", "water", "grass")
Pikachu = Card("Pikachu", 35, 35, 100, ["Tackle", "QuickAttack", "ElectroBall", "Thunder"], "electric", "ground", "electric")






def main():
	print "In the blue corner, weighing 153 pounds, the one, the only Chaaarmander"
	print Charmander.name
	print Charmander.health
	print Charmander.stamina
	print Charmander.attacks
	print Charmander.poketype
	print Charmander.weakness
	print Charmander.resistance
	print "And his challenger, our furry electric ball. You might know him as vagina,,"
	print "PPPIIIKKAACCHHUU"
	print Pikachu.name
	print Pikachu.health
	print Pikachu.stamina
	print Pikachu.attacks
	print Pikachu.poketype
	print Pikachu.weakness
	print Pikachu.resistance

if __name__ == "__main__":
    main()
