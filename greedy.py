from classes import *

def getSymbol(autos):
    lastsymbol = autos[-1].getSymbol()
    if (lastsymbol[-1] == 'Z'):
        for x in range(2, len(lastsymbol)):
            if (not lastsymbol[-x] == 'Z'):
                newsymbol = chr((ord(lastsymbol[-x]) + 1))
                return newsymbol
        newsymbol = ""
        for x in range(len(lastsymbol)+1):
            newsymbol += 'A'

    else:
        return chr(ord(lastsymbol[-1]) + 1)




automatons = []
try:
    _s_pos = open("regex.txt", "r")
    _s_neg = open("regex-.txt", "r")
    s_pos = s_neg = []
    s_pos = [line.rstrip('\n') for line in _s_pos]
    s_neg = [line.rstrip('\n') for line in _s_neg]
    _s_pos.close()
    _s_neg.close()
except:
    print("File not found!")
    exit()
automatons.append(buildAutomatonFromStrings(s_pos, "A"))
