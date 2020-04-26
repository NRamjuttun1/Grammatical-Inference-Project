from classes import *
import random

def fold(auto, merged_node): #additional strain testing required
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
                        auto.removeNode(m)
        if (len(repeats) == 0):
            check = True



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
    newauto.addTransition(newauto.nodes[5], newauto.nodes[6], "c")
    newauto.addEnd(newauto.getNode(6))
    for x in range(3):
        newauto.addNode()
    newauto.addTransition(newauto.nodes[0], newauto.nodes[8], "a")
    newauto.addTransition(newauto.nodes[8], newauto.nodes[9], "a")
    newauto.addTransition(newauto.nodes[9], newauto.nodes[10], "a")
    fold(newauto, newauto.getNode(0))
    print("{} \n\n\n".format(newauto))
    newauto.mergeNode(newauto.getNode(0), newauto.findNode(newauto.symbol + "6"))
    print(newauto)

#foldTest()
cauto = cAutomaton("A")
cauto.addNode()
cauto.getNode(0).promote()
cauto.getNode(0).promote()
cauto.getNode(1).promote()
print(cauto)
print(cauto.copyAutomaton("e"))
