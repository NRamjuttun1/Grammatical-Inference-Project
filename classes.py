class Automaton:

    def __init__(self, ssymbol):
        self.symbol = ssymbol
        self.nodes = []
        self.transitions = []
        self.size = 0
        self.name = 0
        self.start = self.addNode(True)
        self.end = []

    def __str__(self):
        sstring = ""
        for x in self.nodes:
            sstring += str(x) + '\n'
        sstring += '\n'
        for y in self.transitions:
            sstring += str(y) + '\n'
        sstring = sstring + "\nStart Node = {} \nFinal Nodes = ".format(self.start)
        for i in self.end:
            sstring += str(i) + " "
        sstring += '\n'
        return sstring

    def getDisplayTranisitions(self):
        sstring = ""
        for x in self.nodes:
            for i in self.findTransFromNode(x):
                sstring += str(i) + '\n'
        return sstring


    def addNode(self, return_node = False):
        newnode = Node("" + str(self.symbol) + str(self.name))
        self.nodes.append(newnode)
        self.size += 1
        self.name += 1
        if (return_node):
            return newnode


    def addTransition(self, sstart, eend, ssymbol):
        newtransistion = Transition(sstart, eend, ssymbol)
        self.addNewTrans(newtransistion)

    def setStart(self, sstart):
        self.start = sstart

    def setEnd(self, end):
        self.end = end

    def addEnd(self, end):
        self.end.append(end)

    def getNode(self, node):
        return self.nodes[node]

    def getAlphabet(self):
        alphabet = []
        for x in self.transitions:
            if (x.getSymbol() not in alphabet):
                alphabet.append(x.getSymbol())
        return alphabet


    def addNewTrans(self, trans):
        if (not self.checkTransExists(trans)):
            self.transitions.append(trans)

    def checkTransExists(self, trans):
        if (trans in self.transitions):
            return True
        return False

    def deleteTransition(self, trans):
        if (self.checkTransExists(trans)):
            self.transitions.remove(trans)

    def getSize(self):
        return self.size

    def getSymbol(self):
        return self.symbol

    def findNodeobj(self, node):
        return self.findNode(node.getID())

    def findNode(self, id):
        for i in range (len(self.nodes)):
            if (not isinstance(id, int)):
                if (self.nodes[i].getID() == id):
                    return self.nodes[i]
            elif (isinstance(id, int)):
                if (self.nodes[i].getNO() == id):
                    return self.nodes[i]

    def removeNode(self, node):
        if node in self.end:
            if (len(self.end) == 1):
                print("Cannot delete final end node")
                return
            else:
                self.end.remove(node)
        if (self.start == node):
            print("Cannot delete start node")
            return
        transto = self.findTransToNode(node)
        transfrom = self.findTransFromNode(node)
        for x in transto:
            self.deleteTransition(x)
        for x in transfrom:
            self.deleteTransition(x)
        self.nodes.remove(node)

    def checkNodeExists(self, nnode):
        try:
            newnode = self.findNode(nnode.getID())
            return True
        except AttributeError:
            return False

    def findTransFromNode(self, node, symbol = False):
        trans = []
        for i in range(len(self.transitions)):
            if (self.transitions[i].start.equals(node)):
                trans.append(self.transitions[i])
        if (symbol == False):
            return trans
        else:
            return_trans = []
            for x in trans:
                if (x.getSymbol() == symbol):
                    return_trans.append(x)
            return return_trans

    def findTransToNode(self, node):
        trans = []
        for i in range(len(self.transitions)):
            if (self.transitions[i].end.equals(node)):
                trans.append(self.transitions[i])
        return trans

    def _checkPathExists(self, currentNode, explored):
        if (len(explored) == len(self.nodes)):
            return False
        explored.append(currentNode)
        if (currentNode in self.end):
            return True
        trans = self.findTransFromNode(currentNode)
        for x in trans:
            if (x.getEnd() in self.end):
                return True
        for x in range(len(trans)):
            check = False
            if (trans[x].getEnd() not in explored):
                check = self._checkPathExists(trans[x].getEnd(), explored)
            if (check):
                return True
        return False

    def checkPathExists(self):
        return self._checkPathExists(self.start, [])


    def checkInput(self, sstring):
        return self._checkInput(sstring, self.start)

    def _checkInput(self, sstring, nnode):
        if (len(sstring) == 0):
            for x in range(len(self.end)):
                if (nnode.equals(self.end[x])):
                    return True
            return False
        #print(nnode.getID() + " -> " + sstring[0])
        trans = self.findTransFromNode(nnode)
        for i in range(len(trans)):
            if (trans[i].getSymbol() == sstring[0]):
                check = self._checkInput(sstring[1:], trans[i].getEnd())
                if (check):
                    return True
        return False


    def checkDeterministic(self):
        for i in self.nodes:
            if (not self.checkNoRepeatTransitions(i)):
                return False
        return True

    def checkNoRepeatTransitions(self, node):
        arr = []
        trans = self.findTransFromNode(node)
        for x in trans:
            arr.append(x.getSymbol())
        if (checkRepeats(arr)):
            return False
        return True

    def checkNoRepeatSymbol(self, transition):
        trans = self.findTransFromNode(transition.getStart())
        for x in trans:
            if (x.getSymbol() == transition.getSymbol()):
                return False
        return True

    def checkInputs(self, arr):
        count = 0
        for i in arr:
            if checkInput(i):
                count += 1
        return count


    def mergeNode(self, node1, node2, returnNode = False):
        #determine whether it is easier to send the ID or the node Object
        print("{} <--------".format(node1 in self.nodes))
        print("{} <--------".format(node2 in self.nodes))
        print(node2)
        newnode = self.addNode(True)
        node1to = self.findTransToNode(node1)
        node1from = self.findTransFromNode(node1)
        node2to = self.findTransToNode(node2)
        node2from = self.findTransFromNode(node2)
        for x in node1to:
            if (x.getStart() == node2):
                self.addTransition(newnode, newnode, x.getSymbol())
            elif (x.getStart() == node1):
                self.addTransition(newnode, newnode, x.getSymbol())
            else:
                self.addTransition(x.getStart(), newnode, x.getSymbol())
        for x in node2to:
            if (x.getStart() == node1):
                self.addTransition(newnode, newnode, x.getSymbol())
            elif (x.getStart() == node2):
                self.addTransition(newnode, newnode, x.getSymbol())
            else:
                self.addTransition(x.getStart(), newnode, x.getSymbol())
        for x in node1from:
            if (not x.getEnd() == node2):
                self.addTransition(newnode, x.getEnd(), x.getSymbol())
        for x in node2from:
            if (not x.getEnd() == node1):
                self.addTransition(newnode, x.getEnd(), x.getSymbol())
        if ((node1 in self.end) or (node2 in self.end)):
            self.addEnd(newnode)
        if ((node1 == self.start) or (node2 == self.start)):
            self.setStart(newnode)
        self.removeNode(node1)
        self.removeNode(node2)
        if (returnNode):
            return newnode

    def fold(self, merged_node):
        check = False
        while(not check == True):
            trans = self.findTransFromNode(merged_node)
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
                    self.addTransition(merged_node, merged_node, i)
                    trans_to_fold = self.findTransFromNode(merged_node, i)
                    end = False
                    for x in trans_to_fold:
                        current_node = x.getEnd()
                        nodes_to_fold = []
                        while(end == False): #traversing each node to get to the end
                            nodes_to_fold.append(current_node)
                            new_trans = self.findTransFromNode(current_node, i)
                            if (len(new_trans) > 1):
                                end = True
                            elif (len(new_trans) == 0):
                                end = True
                            elif(len(new_trans) == 1):
                                if (new_trans[0].getEnd() not in nodes_to_fold) and (not trans[0].getEnd() == merged_node ):
                                    current_node = new_trans[0].getEnd()
                                else:
                                    end = True
                        if (merged_node in nodes_to_fold):
                            nodes_to_fold.remove(merged_node)
                        for m in nodes_to_fold:
                            get_trans = self.findTransFromNode(m)
                            for x in get_trans:
                                #if (not x.getEnd() == merged_node):
                                    #if (x.getSymbol() == i):
                                    #    print("Deleted Transition {}".format(x))
                                    #    self.deleteTransition(x)
                                if(x.getEnd() in nodes_to_fold):
                                    if (not self.checkTransExists(Transition(merged_node, merged_node, x.getSymbol()))):
                                        x.setStart(merged_node)
                                        x.setEnd(merged_node)
                                    else:
                                        self.deleteTransition(x)
                                else:
                                    if (not self.checkTransExists(Transition(merged_node, x.getEnd(), x.getSymbol()))):
                                        x.setStart(merged_node)
                                    else:
                                        self.deleteTransition(x)
                                print("REPEAT")
                        for m in nodes_to_fold:
                            print("REPEAT")
                            if (m in self.end):
                                if (merged_node not in self.end):
                                    self.addEnd(merged_node)
                            if (m == self.start):
                                self.setStart(merged_node)
                            print("REMOVED")
                            self.removeNode(m)
            if (len(repeats) == 0):
                    check = True
        return self



    def getNodePos(self, node):
        for x in range(len(self.nodes)):
            if (self.nodes[x] == node):
                return x

    def copyAutomaton(self, symbol):
        newauto = Automaton(symbol)
        return self._copyAutomaton(newauto)

    def _copyAutomaton(self, newauto):
        for x in range(self.getSize()-1):
            newauto.addNode()
        for i in self.transitions:
            newauto.addTransition(newauto.nodes[self.getNodePos(i.getStart())], newauto.nodes[self.getNodePos(i.getEnd())], i.getSymbol())
        newauto.setStart(newauto.nodes[self.getNodePos(self.start)])
        for f in self.end:
            newauto.addEnd(newauto.nodes[self.getNodePos(f)])
        return newauto

    def getComplementAutomaton(self, terminate = False):
        newauto = self.copyAutomaton("_{}_".format(self.getSymbol()))
        alphabet = newauto.getAlphabet()
        terminating = newauto.addNode(True)
        newend = []
        for x in newauto.nodes:
            ab = alphabet.copy()
            for j in newauto.findTransFromNode(x):
                ab.remove(j.getSymbol())
            for i in ab:
                newauto.addTransition(x, terminating, i)
            if (x not in newauto.end):
                newend.append(x)
        newauto.setEnd(newend)
        if (terminate):
            return newauto, terminating
        return newauto


class cAutomaton(Automaton):

    def __init__(self, idd):
        super().__init__(idd)

    def __str__(self):
        sstring = ""
        for x in self.nodes:
            sstring += str(x) + '\n'
        sstring = sstring + '\n'
        for y in self.transitions:
            sstring += y.getStart().displayNode() + " -" + y.getSymbol()+ "-> " + y.getEnd().displayNode() + '\n'
        sstring += "\nStart Node = {} \nFinal Nodes = ".format(self.start.displayNode())
        for i in self.end:
            sstring += i.displayNode() + " "
        sstring += '\n'
        return sstring

    def returnSimpleString(self):
        sstring = ""
        for x in self.nodes:
            sstring += str(x) + '\n'
        sstring = sstring + '\n'
        for y in self.transitions:
            sstring += y.getStart().displayNode() + " -" + y.getSymbol()+ "-> " + y.getEnd().displayNode() + '\n'
        sstring += "\nStart Node = {} \nFinal Nodes = ".format(self.start.displayNode())
        for i in self.end:
            sstring += str(i.displayNode()) + " "
        sstring += '\n'
        return sstring

    def addNode(self, return_node = False):
        newnode = colourNode("" + str(self.symbol) + str(self.name))
        self.nodes.append(newnode)
        self.size += 1
        self.name += 1
        if (return_node):
            return newnode

    def getAllWhiteNodes(self):
        whites = []
        for x in self.nodes:
            if (x.checkLevel() == 0):
                whites.append(x)
        return whites

    def getAllBlueNodes(self):
        blues = []
        for x in self.nodes:
            if (x.checkLevel() == 1):
                blues.append(x)
        return blues

    def getAllRedNodes(self):
        reds = []
        for x in self.nodes:
            if (x.checkLevel() == 2):
                reds.append(x)
        return reds

    def copyAutomaton(self, symbol):
        newauto = cAutomaton(symbol)
        newauto = super()._copyAutomaton(newauto)
        for x in self.getAllRedNodes():
            newauto.findNode(str(symbol) + str(x.getNO())).promote()
            newauto.findNode(str(symbol) + str(x.getNO())).promote()
        for x in self.getAllBlueNodes():
            newauto.findNode(str(symbol) + str(x.getNO())).promote()
        return newauto



class Node:

    def __init__(self, iid):
        self.id = iid

    def __str__(self):
        return "Node : "+ self.getID()

    def displayNode(self):
        return "Node : "+ self.getID()

    def getID(self):
        return self.id

    def getNO(self):
        return int(self.id[1:])

    def equals(self, node):
        return (self.id == node.getID())

class colourNode(Node):

    def __init__(self, iid):
        super().__init__(iid)
        self.colour = 0

    def __str__(self):
        return "cNode : {} - State : {}".format(str(self.getID()), str(self.getState()))

    def displayNode(self):
        return "cNode : {}".format(str(super().getID()))

    def promote(self):
        if (not self.colour == 2):
            self.colour += 1
            return True
        else:
            print("Cannot promote red state")
        return False

    def checkLevel(self):
        return self.colour

    def getState(self):
        if (self.checkLevel() == 0):
            return "White"
        elif (self.checkLevel() == 1):
            return "Blue"
        return "Red"


class Transition:

    def __init__(self, sstart, eend, ssymbol):
        self.start = sstart
        self.end = eend
        self.symbol = ssymbol

    def __str__(self):
        return self.getStart().displayNode() + " -" + str(self.getSymbol()) + "-> " + self.getEnd().displayNode()

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getSymbol(self):
        return self.symbol

    def setStart(self, node):
        self.start = node

    def setEnd(self, node):
        self.end = node

    def __eq__(self, obj):
        return ((obj.start == self.start) and (obj.end == self.end) and (obj.symbol == self.symbol))

def buildcAutomatonFromStrings(sstrings, ssymbol):
    auto = cAutomaton(ssymbol)
    return _buildAutomatonFromStrings(auto, sstrings)

def buildAutomatonFromStrings(sstrings, ssymbol):
    auto = Automaton(ssymbol)
    return _buildAutomatonFromStrings(auto, sstrings)

def _buildAutomatonFromStrings(auto, strings):
    for i in strings:
        _buildAutomatonFromString(i, auto)
    return auto

def _buildAutomatonFromString(sstring, auto):
    auto.addNode()
    endNode = auto.findNode("" + str(auto.symbol) + str(auto.size - 1))
    auto.addTransition(auto.start, endNode, sstring[0])
    for i in range(len(sstring)-1): #change here to remove sstring[1:]
        startNode = auto.findNode("" + str(auto.symbol) + str(auto.size - 1))
        auto.addNode()
        endNode = auto.findNode("" + str(auto.symbol) + str(auto.size - 1))
        auto.addTransition(startNode, endNode, sstring[i+1]) #change here for sstring[i] to i+1
    auto.end.append(endNode)

def buildPTA(sstrings, ssymbol):
    newauto = cAutomaton(ssymbol)
    for x in sstrings:
        newauto = buildPTA2(x, newauto, newauto.start)
    return newauto

def buildPTA2(str, newauto, current_node):
    for letter in str:
        trans = newauto.findTransFromNode(current_node, letter)
        if (len(trans) > 1):
            print(newauto.checkDeterministic())
            print("Determinism lost")
            print(newauto)
            exit()
        elif (len(trans) == 1):
            current_node = trans[0].getEnd()
        elif(len(trans) == 0):
            new_node = newauto.addNode(True)
            newauto.addTransition(current_node, new_node, letter)
            current_node = new_node
    newauto.addEnd(current_node)
    return newauto

def checkExists(arr, el):
    for item in arr:
        if (item == el):
            return True
    return False

def mergeAutomaton(auto, arr):
    temparr = []
    for item in arr:
        if (not(checkExists(temparr,item))):
            temparr.append(item)
    nlist = [[] for i in range(len(temparr))]
    for i in range(len(arr)):
        try:
            nlist[arr[i]].append(i) #appends position number to nlist[value] list
        except(IndexError):
            print("Value of i is {} and the max length of the nlist is {}".format(arr[i], len(nlist)))
            print("Length of arr is {} and it contains {}".format(len(arr), arr))
            exit()
    return buildAutomatonFromMergeList(nlist, auto)

def findNewNodeFromMerge(auto, arr, node):
    nodesymbol = node.getNO()
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if (arr[x][y] == nodesymbol):
                return x

def buildAutomatonFromMergeList(arr, auto):
    newauto = Automaton("T")
    for g in range(len(arr) - 1):
        newauto.addNode()
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            trans = auto.findTransFromNode(auto.findNode("" + auto.symbol + str(arr[i][j])))
            for x in range(len(trans)):
                newauto.addTransition(newauto.nodes[i], newauto.nodes[findNewNodeFromMerge(auto, arr, trans[x].getEnd())], trans[x].getSymbol())
                #go to trans.end find the destination node and map that to the new node and then create a new transition between the two using the same symbol
    newauto.start = newauto.nodes[findNewNodeFromMerge(auto, arr, auto.start)]
    for m in range(len(auto.end)):
        newauto.end.append(newauto.nodes[findNewNodeFromMerge(auto, arr, auto.end[m])])
    return newauto

def getListPos(arr, el):
    for x in range(len(arr)):
        if (arr[x] == el):
            return x

def flattenMergeList(arr):
    templist = []
    for x in arr:
        if (not(x in templist)):
            templist.append(x)
    templist.sort()
    for x in range(len(arr)):
        arr[x] = getListPos(templist, arr[x])
    return arr

def checkRepeats(arr):
    list = []
    for x in arr:
        if (not x in list):
            list.append(x)
        elif (x in list):
            return True
    return False

def find2Min(fitnessarr):
    min1 = 0
    min2 = 1
    for i in range(len(fitnessarr)):
        if (fitnessarr[i] < fitnessarr[min2]):
            if (fitnessarr[i] < fitnessarr[min1]):
                min1 = i
            else:
                if (not min1 == i):
                    min2 = i
    return min1, min2


def findMax(fitnessarr, ignore = []):
    max = 0
    for i in range(len(fitnessarr)):
        if (i not in ignore):
            if (fitnessarr[i] > fitnessarr[max]):
                max = i
    return max

def findMin(fitnessarr):
    min = 0
    for i in range(len(fitnessarr)):
        if (fitnessarr[i] < fitnessarr[min]):
            min = i
    return min

def find2Max(fitnessarr, ignore = []):
    max1 = 0
    max2 = 1
    for i in range(len(fitnessarr)):
        if (fitnessarr[i] > fitnessarr[max2]):
            if (fitnessarr[i] > fitnessarr[max1]):
                if (i not in ignore):
                    max1 = i
            else:
                if (i not in ignore):
                    max2 = i
    return max1, max2
