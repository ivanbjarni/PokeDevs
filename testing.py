from Attack import *
from Card import *
from Deck import *
from Hand import *
from Player import *


print "Hello"
Charmander = Card("Charmander", 39, 39, 90, ["Growl", "FireFang", "Flamethrower", "Inferno"], "fire", "water", "grass")
print Charmander.name
print Charmander.healthMax
print Charmander.stamina
print Charmander.attacks
print Charmander.poketype
print Charmander.weakness
print Charmander.resistance

