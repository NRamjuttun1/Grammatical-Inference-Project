from classes import *
import time

def getSymbol(arr = []):
    if len(arr) == 0:
        return "A"
    new_count = 1
    last_symbol = arr[-1][0].getSymbol()
    for x in last_symbol:
        if x == "_":
            new_count += 26
        else:
            new_count += ord(x) - 65
    new_symbol = ""
    for i in range(new_count//26):
        new_symbol += "_"
    new_symbol += chr((new_count%26) + 65)
    return new_symbol

def buildPTAFromStrings(sstrings):
    return buildPTA(sstrings, getSymbol())

def promoteNode(node):
    if (node.promote()):
        if (node.checkLevel() == 2):
            red_nodes.insert(0, node)
            blue_nodes.remove(node)
        elif (node.checkLevel() == 1):
            blue_nodes.insert(0, node)
            white_nodes.remove(node)

def getScore(auto):
    if (not auto.checkInputs(s_neg) == 0) or (not auto.checkInputs(s_pos) == len(s_pos)):
        return -1
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

def fillBluesnotwork(node, auto):
    trans = auto.findTransFromNode(node)
    for p in trans:
        print(p)
    print("Filling blues from {}".format(node))
    if (len(trans) == 0):
        if (node.checkLevel() == 1):
            promoteNode(node)
    check = False
    for x in trans:
        if (x.getEnd().checkLevel() == 0):
            if (x.getEnd() not in white_nodes):
                print("FUCK NO : {}".format(x.getEnd()))
            promoteNode(x.getEnd())
            check = True
    if (not check):
        end = False
        for x in trans:
            y = x.getEnd()
            while(not end):
                if (y.checkLevel() == 0):
                    promoteNode(y)
                    end = True
                    if (node.checkLevel() == 1):
                        promoteNode(node)
                    return False
                elif (len(auto.findTransFromNode(y)) == 0):
                    end = True
                else:
                    return fillBlues(y, auto)
        print("Forced End")
        return True
    return False

def fillBlues(node, auto):
  if checkWin(auto):
      return True
  if (len(auto.getAllWhiteNodes()) == 0):
      if (len(auto.getAllBlueNodes()) == 0):
          return True
      else:
          return False
  else:
      promoteNode(auto.getAllWhiteNodes()[0])
      return False

def updateStateLists(auto):
    red_nodes = auto.getAllRedNodes()
    blue_nodes = auto.getAllBlueNodes()
    white_nodes = auto.getAllWhiteNodes()
    return red_nodes, blue_nodes, white_nodes

def checkWin(auto):
    if (len(auto.getAllWhiteNodes()) == 0) and (len(auto.getAllBlueNodes()) == 0):
        if (len(auto.getAllRedNodes()) == len(auto.nodes)):
            return True
    return False

def findNodeFromCopyAuto(original, copied, node):
    return copied.findNode(node.getNO())

def findMinScore(autos):
    min = 0
    while(autos[min][1] == -1):
        min += 1
        if (min == len(autos)):
            return False
    for x in range(len(autos)):
        if ( not autos[x][1] == -1):
            if autos[x][1] < autos[min][1]:
                min = x
    return min

def removeAllWithList(ls, ls_delete):
    return_ls = []
    for x in ls:
        if (x not in ls_delete):
            return_ls.append(x)
    return return_ls

def printListLengths():
    print("Whites : {}".format(len(white_nodes)))
    print("Blues : {}".format(len(blue_nodes)))
    print("Reds : {}".format(len(red_nodes)))


start_time = time.time()
try:
    _s_pos = open("ex+.txt", "r")
    _s_neg = open("ex-.txt", "r")
    _u_pos = open("ex+_u.txt", "r")
    _u_neg = open("ex-_u.txt", "r")
    s_pos = []
    s_neg = []
    u_pos = []
    u_neg = []
    s_pos = [line.rstrip('\n') for line in _s_pos]
    s_neg = [line.rstrip('\n') for line in _s_neg]
    u_pos = [line.rstrip('\n') for line in _u_pos]
    u_neg = [line.rstrip('\n') for line in _u_neg]
    _s_pos.close()
    _s_neg.close()
    _u_pos.close()
    _u_neg.close()
except():
    print("File not found!")
    exit()
automatons = []
pta = buildPTAFromStrings(s_pos)
print("Original PTA : \n{}".format(pta))
automatons.append([pta, getScore(pta)])
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
hold = pta.start
check = False
its = 0
while (check == False):
    valid_autos = []
    temp_autos = []
    print("Iteration : {}".format(its))
    check = fillBlues(current, pta)
    red_nodes, blue_nodes, white_nodes = updateStateLists(pta)
    printListLengths()
    if (not check):
        if (len(blue_nodes) > 1):
            print("More than one current blue node")
        x = blue_nodes[0]
        temp_autos.append([pta, getScore(pta)])
        for y in red_nodes:
            copy_auto = pta.copyAutomaton(getSymbol(temp_autos))
            current_blue = findNodeFromCopyAuto(pta, copy_auto, x)
            current_red = findNodeFromCopyAuto(pta, copy_auto, y)
            merge_node = copy_auto.mergeNode(current_blue, current_red, True)
            merge_node.promote()
            copy_auto.fold(merge_node)
            copy_auto.delete_unused_nodes()
            temp_autos.append([copy_auto, getScore(copy_auto)])
        valid_autos = []
        for i in range(1, len(temp_autos)):
            if (not temp_autos[i][1] == -1):
                valid_autos.append(temp_autos[i])
        if (len(valid_autos) == 0):
            promoteNode(x)
        else:
            new_pta = valid_autos[findMinScore(valid_autos)]
            pta = new_pta[0].copyAutomaton(getSymbol())
            red_nodes, blue_nodes, white_nodes = updateStateLists(pta)
    pta.delete_unused_nodes()
    its += 1

pta.delete_unused_nodes()
print(pta)
print(len(pta.transitions))
if pta.checkInputs(s_neg) == 0:
    print("Correctly rejects all negative words")
if pta.checkInputs(s_pos) == len(s_pos):
    print("Correctly accepts all postive words")
timed = ("--- %s seconds ---" % (time.time() - start_time))
print(its)
