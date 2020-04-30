from classes import *
import random


def test():
    newauto = Automaton("G")
    for x in range(3):
        newauto.addNode()
    newauto.addTransition(newauto.nodes[0], newauto.nodes[1], "a")
    newauto.addTransition(newauto.nodes[0], newauto.nodes[3], "b")
    newauto.addTransition(newauto.nodes[0], newauto.nodes[2], "c")
    newauto.addTransition(newauto.nodes[2], newauto.nodes[0], "d")
    newauto.addTransition(newauto.nodes[2], newauto.nodes[1], "e")
    newauto.addTransition(newauto.nodes[1], newauto.nodes[3], "f")
    newauto.setStart(newauto.getNode(2))
    newauto.addEnd(newauto.getNode(3))
    print(newauto)
    compauto = newauto.getComplementAutomaton()
    print(compauto)
    input = "dcdcdcdcdcdcdcdcdb"
    print("Automaton accepts input -> {} \nComplement Automaton accepts input -> {}".format(newauto.checkInput(input), compauto.checkInput(input)))
    trans = newauto.findTransFromNode(newauto.getNode(2), "d")
    for x in trans:
        print("Start : {}, End : {}, Symbol : {}".format(x.getStart(), x.getEnd(), x.getSymbol()))

def foldTest():
    newauto = cAutomaton("P")
    for x in range(7):
        newauto.addNode()
    newauto.addTransition(newauto.nodes[0], newauto.nodes[1], "a")
    newauto.addTransition(newauto.nodes[0], newauto.nodes[7], "a")
    newauto.addTransition(newauto.nodes[1], newauto.nodes[2], "a")
    newauto.addTransition(newauto.nodes[2], newauto.nodes[3], "a")
    newauto.addTransition(newauto.nodes[2], newauto.nodes[0], "b")
    newauto.addTransition(newauto.nodes[3], newauto.nodes[4], "a")
    newauto.addTransition(newauto.nodes[4], newauto.nodes[5], "a")
    newauto.addTransition(newauto.nodes[5], newauto.nodes[6], "d")
    newauto.addEnd(newauto.getNode(6))
    for x in range(4):
        newauto.addNode()
    newauto.addTransition(newauto.nodes[0], newauto.nodes[8], "c")
    newauto.addTransition(newauto.nodes[8], newauto.nodes[9], "a")
    newauto.addTransition(newauto.nodes[9], newauto.nodes[10], "a")
    newauto.addTransition(newauto.nodes[7], newauto.nodes[11], "c")
    m = newauto.mergeNode(newauto.getNode(2), newauto.getNode(1), True)
    print("{}\n".format(m))
    print(newauto)
    newauto.fold(m)
    print(newauto)

def readinexamples():
    try:
        _s_pos = open("ex+.txt", "r")
        _s_neg = open("ex-.txt", "r")
        _u_pos = open("regex+_u.txt", "r")
        _u_neg = open("regex-_u.txt", "r")
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
        pta = buildPTA(s_pos, "F")
    except():
        print("File not found!")
        exit()
    return s_pos, s_neg, u_pos, u_neg, pta

s_pos, s_neg, u_pos, u_neg, pta = readinexamples()

#foldTest()
