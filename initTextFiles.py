from Presets import *

p = Presets()

def createPokemonCounterFile(name):
	with open(name, "a") as myfile:
		for i in xrange(1,152):
			myfile.write(p.gc(i).name+" 0\n")
		myfile.close()

createPokemonCounterFile("pokemonKillers.txt")
createPokemonCounterFile("pokemonVictims.txt")
createPokemonCounterFile("pokemonPlayed.txt")