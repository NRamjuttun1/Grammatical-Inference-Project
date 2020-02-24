class Automaton:

    def __init__(self, ssymbol):
        self.symbol = ssymbol
        self.nodes = []
        self.transitions = []
        self.size = 0
        self.name = 0
        self.addNode()
        self.start = self.nodes[0]
        self.end = []

    def __str__(self):
        sstring = ""
        for x in self.nodes:
            sstring = sstring + str(x) + '\n'
        sstring = sstring + '\n'
        for y in self.transitions:
            sstring = sstring + str(y.getStart()) + " -" + str(y.getSymbol()) + "-> " + str(y.getEnd()) + '\n'
        sstring = sstring + "Start Node = {} '\n' Final Nodes = ".format(self.start)
        for i in self.end:
            sstring = sstring + str(i) + " "
        return sstring

    def addNode(self):
        newnode = Node("" + str(self.symbol) + str(self.name))
        self.nodes.append(newnode)
        self.size = self.size + 1
        self.name = self.name + 1

    def addTransition(self, sstart, eend, ssymbol):
        newtransistion = Transition(sstart, eend, ssymbol)
        self.transitions.append(newtransistion)

    def getSize(self):
        return self.size

    def findNode(self, id):
        for i in range (len(self.nodes)):
            if (self.nodes[i].getID() == id):
                return self.nodes[i]

    def checkNodeExists(self, nnode):
        try:
            newnode = self.findNode(nnode.getID())
            return True
        except AttributeError:
            return False

    def findTransFromNode(self, node):
        trans = []
        for i in range(len(self.transitions)):
            if (self.transitions[i].start.equals(node)):
                trans.append(self.transitions[i])
        return trans

    def findTransToNode(self, node):
        trans = []
        for i in range(len(self.transitions)):
            if (self.transitions[i].end.equals(node)):
                trans.append(self.transitions[i])
        return trans

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
            arr = []
            trans = findTransFromNode(i)
            for x in trans:
                arr.append(x.getSymbol())
            if (checkRepeats(arr)):
                return False
        return True

    def checkInputs(self, arr):
        count = 0
        for i in arr:
            if checkInput(i):
                count += 1
        return count


class Node:

    def __init__(self, iid):
        self.id = iid

    def __str__(self):
        return "Node : "+ self.id

    def getID(self):
        return self.id

    def getNO(self):
        return int(self.id[1:])

    def equals(self, node):
        return (self.id == node.getID())


class Transition:

    def __init__(self, sstart, eend, ssymbol):
        self.start = sstart
        self.end = eend
        self.symbol = ssymbol

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getSymbol(self):
        return self.symbol


def buildAutomatonFromStrings(sstrings, ssymbol):
    auto = Automaton(ssymbol)
    for i in range(len(sstrings)):
        _buildAutomatonFromString(sstrings[i], auto)
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
        if (  not (x in list)):
            list.append(x)
        elif (x in list):
            return True
    return False
