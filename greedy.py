from classes import *

def getSymbol():
    if (len(automatons) == 0):
        return "A"
    lastsymbol = automatons[-1].getSymbol()
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
    return buildPTA(sstrings, getSymbol())

def promoteNode(node):
    if (node.promote()):
        if (node.checkLevel() == 2):
            red_nodes.append(node)
            blue_nodes.remove(node)
        elif (node.checkLevel() == 1):
            blue_nodes.append(node)
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


def fold(auto, merged_node):
    check = False
    while(not check == True):
        trans = auto.findTransFromNode(merged_node)
        symbols = []
        repeats = []
        for x in trans:
            if (x.getSymbol() not in symbols):
                symbols.append(x.getSymbol())
            elif (x.getSymbol() in symbols):
                repeats.append(x.getSymbol())
        if (len(repeats) == 0):
            check = True
        if (check == False):
            for i in repeats:
                auto.addTransition(merged_node, merged_node, i)
                trans_to_fold = auto.findTransFromNode(merged_node, i)
                end = False
                for x in trans_to_fold:
                    current_node = x.getEnd()
                    nodes_to_fold = []
                    while(end == False):
                        print("Current Node : {}".format(current_node))
                        nodes_to_fold.append(current_node)
                        new_trans = auto.findTransFromNode(current_node, i)
                        if (len(new_trans) > 1):
                            print(auto.checkDeterministic())
                            print("Determinism not reached multiple transitions from Node : {} with the symbol {}".format(current_node, x.getSymbol()))
                            exit()
                        if (len(new_trans) == 0):
                            end = True
                            print("Got to end of branch")
                        elif(len(new_trans) == 1):
                            current_node = new_trans[0].getEnd()
                    for m in nodes_to_fold:
                        get_trans = auto.findTransFromNode(m)
                        for x in get_trans:
                            if (x.getSymbol() == i):
                                auto.deleteTransition(x)
                            elif(x.getEnd() in nodes_to_fold):
                                x.setStart(merged_node)
                                x.setEnd(merged_node)
                            else:
                                x.setStart(merged_node)
                                print("Number of transitions still attached from removed Node {} : {}".format(m,len(auto.findTransFromNode(m))))
                                print(m)
                    for m in nodes_to_fold:
                        if (m in auto.end):
                            if (merged_node not in auto.end):
                                auto.addEnd(merged_node)
                        if (m == auto.start):
                            auto.setStart(merged_node)
                        auto.removeNode(m)
        print(auto)
        if (len(repeats) == 0):
            check = True
    return auto



automatons = []
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
printStates(1)
