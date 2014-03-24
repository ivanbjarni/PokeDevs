def isNumber(x):
	return isinstance(x, (int, long, float, complex))

def pokemonCounterLog(lookup,file):
	with open(file) as myFile:
	    for num, line in enumerate(myFile, 1):
	        if lookup in line:
	            replace_line( file, num-1, lookup +" "+ str( int(line[len(lookup):]) + 1)+"\n" )


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()