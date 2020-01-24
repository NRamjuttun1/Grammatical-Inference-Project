class Automaton:

    def __init__(self, ssymbol):
        self.symbol = ssymbol
        self.nodes = []
        self.nodes.append(Node("" + self.symbol + '0'))
        self.transitions = []
        self.size = 1
        self.start = self.nodes[0]
        self.end = []

    def addNode(self ):
        newnode = Node("" + self.symbol + self.size)
        nodes.add(newnode)
        size = size + 1

    def addTransition(self, sstart, eend, ssymbol):
        newtransistion = Transition(sstart, eend, ssymbol)
        transitions.add(newtransistion)

    def size(self):
        return len(nodes)

    def findNode(self, id):
        for i in range (len(self.nodes)):
            if (node[i].getID() == id):
                return node[i]

    def checkNodeExists(self, nnode):
        if (self.findNode(nnode.getID()) != None): #NOT DEFINED HERE
            return True
        else:
            return False

    def findTransFromNode(self, node):
        trans = []
        for i in range(len(transitions)):
            if (transitions[i].start.equals(node)):
                trans.append(transitions[i])
        return trans

    def findTransToNode(self, node):
        trans = []
        for i in range(len(transitions)):
            if (transitions[i].end.equals(node)):
                trans.append(transitions[i])
        return trans

    def checkInput(self, sstring):
        _checkInput(sstring, self.start)

    def _checkInput(self, sstring, nnode):
        trans = findTransFromNode(nnode)
        for i in range(len(trans)):
            if (trans[i].getSymbol() == sstring[0]):
                if (_checkInput(sstring[1:], trans[i].getEnd())):
                    return True
        return False

    def buildAutomatonFromStrings(self, sstrings):
        for i in range(sstrings):
            buildAutomatonFromString(sstrings[i])

    def buildAutomatonFromString(self, sstring):
        addNode()
        endNode = findNode("" + self.symbol + (self.size - 1))
        addTransition(self.start, endNode, sstring[0])
        for i in range(len(sstring[1:])):
            startNode = findNode("" + self.symbol + (self.size - 1))
            addNode()
            endNode = findNode("" + self.symbol + (self.size - 1))
            addTransition(startNode, endNode, sstring[i])




class Node:

    def __init__(self, iid):
        self.id = iid

    def getID(self):
        return self.id

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

auto = Automaton("s")
node = Node("d7")
auto.checkNodeExists(node)
