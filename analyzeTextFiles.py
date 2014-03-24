from util import *
pokemons = []
played = []
killers = []
victims = []
stat = []
meanStat = 0
varStat = 0


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
		if victims[num-1]>0:
			stat.append( (killers[num-1])/(victims[num-1]) )
		else:
			stat.append(-1)

d = dict(zip(pokemons, stat))

rank = 0
for w in sorted(d, key=d.get, reverse=True):
	rank +=1
	print rank,": ",w, d[w]

meanStat = mean(stat)
varStat= var(stat, meanStat)
print meanStat, varStat