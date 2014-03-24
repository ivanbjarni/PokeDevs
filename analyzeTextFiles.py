pokemons = []
played = []
killers = []
victims = []
stat = []



with open("pokemonPlayed.txt") as myFile:
	for num, line in enumerate(myFile, 1):
		i = line.index(' ')
		pokemons.append(line[:i])
		played.append(float(line[i:]))

with open("pokemonKillers.txt") as myFile:
	for num, line in enumerate(myFile, 1):
		i = line.index(' ')
		killers.append(float(line[i:]))

with open("pokemonVictims.txt") as myFile:
	for num, line in enumerate(myFile, 1):
		i = line.index(' ')
		pokemons.append(line[:i])
		victims.append(int(line[i:]))
		if victims[num-1]+killers[num-1]>0:
			stat.append( (killers[num-1]-victims[num-1])/(victims[num-1]+killers[num-1]) )
		else:
			stat.append(0)

d = dict(zip(pokemons, stat))

rank = 1
for w in sorted(d, key=d.get, reverse=True):
	rank +=1
	print rank,": ",w, d[w]