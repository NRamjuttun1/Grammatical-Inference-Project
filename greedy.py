from classes import *

def getSymbol(automatons):
    if (len(automatons) == 0):
        return "A"
    lastsymbol = automatons[-1][0].getSymbol()
    if (lastsymbol[-1] == 'Z'):
        for x in range(2, len(lastsymbol)):
            if (not lastsymbol[-x] == 'Z'):
                newsymbol = chr((ord(lastsymbol[-x]) + 1))
                return newsymbol
        newsymbol = ""
        for x in range(len(lastsymbol)+1):
            newsymbol += 'A'
            return newsymbol
    else:
        return chr(ord(lastsymbol[-1]) + 1)

def buildPTAFromStrings(sstrings):
    return buildPTA(sstrings, getSymbol([]))

def promoteNode(node):
    if (node.promote()):
        if (node.checkLevel() == 2):
            red_nodes.insert(0, node)
            blue_nodes.remove(node)
        elif (node.checkLevel() == 1):
            blue_nodes.insert(0, node)
            white_nodes.remove(node)

def getScore(auto):
    score = 0
    score += len(auto.nodes)
    score += len(auto.transitions)
    return score

def printStates(hideWhites = False):
    print("Red Nodes : ")
    for x in red_nodes:
        print(x)
    print("\nBlue Nodes")
    for x in blue_nodes:
        print(x)
    if (hideWhites == False):
        print("\nWhite Nodes")
        for x in white_nodes:
            print(x)

def fillBlues(trans, node):
    if (len(trans) == 0):
        if (node.checkLevel() == 1):
            promoteNode(node)
    check = False
    for x in trans:
        if (x.getEnd().checkLevel() == 0):
            promoteNode(x.getEnd())
            check = True
    if (not check):
        if (node.checkLevel() == 1):
            promoteNode(node)

def checkFinished():
    if (len(white_nodes) == 0) and (len(blue_nodes) == 0):
        return True
    return False

def updateStateLists(auto):
    red_nodes = auto.getAllRedNodes()
    blue_nodes = auto.getAllBlueNodes()
    white_nodes = auto.getAllWhiteNodes()






try:
    #_s_pos = open("regex.txt", "r")
    #_s_neg = open("regex-.txt", "r")
    _s_pos = open("ex+.txt", "r")
    _s_neg = open("ex-.txt", "r")
    s_pos = s_neg = []
    s_pos = [line.rstrip('\n') for line in _s_pos]
    s_neg = [line.rstrip('\n') for line in _s_neg]
    _s_pos.close()
    _s_neg.close()
except:
    print("File not found!")
    exit()
pta = buildPTAFromStrings(s_pos)
white_nodes = []
blue_nodes = []
red_nodes = []
for x in pta.nodes[1:]:
    white_nodes.append(x)
red_nodes.append(pta.start)
pta.start.promote()
pta.start.promote()
num_nodes = len(white_nodes) + len(red_nodes) + len(blue_nodes)
current = pta.start
check = False
while(check == False):
    fillBlues(pta.findTransFromNode(current), current)
    auto_list = [[]]
    auto_list.append([pta, getScore(pta), None])
    for x in blue_nodes:
        for j in red_nodes:
            print("Blue Node : {} \nRed Node : {}".format(x, j))
            new_auto = pta.copyAutomaton(getSymbol(auto_list))
            merge_node = new_auto.mergeNode(new_auto.findNode(str(new_auto.symbol) + str(x.getNO())), new_auto.findNode(str(new_auto.symbol) + str(j.getNO())), True)
            print(new_auto)
            print("Node that has been merged : {}".format(merge_node))
            new_auto.fold(merge_node)
            auto_list.append([new_auto, getScore(new_auto), merge_node])
            print(new_auto)
    check = True
