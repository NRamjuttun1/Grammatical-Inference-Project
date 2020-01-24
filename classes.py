class Automaton:

    def __init__(self, ssymbol):
        self.symbol = ssymbol
        self.nodes = []
        self.nodes.append(Node("" + str(self.symbol) + '0'))
        self.transitions = []
        self.size = 1
        self.name = 1
        self.start = self.nodes[0]
        self.end = []

    def addNode(self):
        newnode = Node("" + str(self.symbol) + str(self.name))
        self.nodes.append(newnode)
        self.size = self.size + 1
        self.name = self.name + 1

    def addTransition(self, sstart, eend, ssymbol):
        newtransistion = Transition(sstart, eend, ssymbol)
        self.transitions.append(newtransistion)

    def size(self):
        return len(nodes)

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


class Node:

    def __init__(self, iid):
        self.id = iid

    def __str__(self):
        return "Node : "+ self.id

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

strs = ["cars", "drives"]
auto = buildAutomatonFromStrings(strs, "s")
print(auto.checkNodeExists(auto.findNode("s10")))
for i in range(len(auto.transitions)):
    if (auto.transitions[i].getStart().getID() == "s3"): 
        print(auto.transitions[i].getSymbol())
