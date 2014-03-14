from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *

Charmander = Card("Charmander", 39, 39, 90, ["Growl", "FireFang", "Flamethrower", "Inferno"], "fire", "water", "grass")
Pikachu = Card("Pikachu", 35, 35, 100, ["Tackle", "QuickAttack", "ElectroBall", "Thunder"], "electric", "ground", "electric")
#CharAttacks
Growl = Attack("Growl", 5, 5, 0, 0, "normal")
FireFang = Attack("FireFang", 10, 12, 0, 2, "fire")
Flamethrower = Attack("Flamethrower", 18, 30, 0, 0, "fire")
Inferno = Attack("Inferno", 25, 50, 0, 0, "fire")
#PikachuAttacks
Tackle = Attack("Tackle", 7, 10, 0, 0, "normal")
QuickAttack = Attack("QuickAttack", 12, 20, 0, 0, "normal")
ElectroBall = Attack("ElectroBall", 18, 30, 0, 0, "electric")
Thunder = Attack("Thunder", 30, 50, 10, 0, "electric")




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
	print "Player 1, your pokemon is Pikachu"
	print "Player 2, your pokemon is Charmander"
	print "But choose wisely..."
	print "I like googling myself... but don't tell anyone"
	print "I also like whiskey 8)"



if __name__ == "__main__":
    main()
