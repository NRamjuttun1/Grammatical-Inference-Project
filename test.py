from classes import *
import random

def getWords(_auto):
    auto, terminating = _auto.getComplementAutomaton(True)
    print("Terminating Node : {}".format(terminating))
    words = []
    for x in range(100):
        current = auto.start
        word = ""
        count = 0
        end = False
        while(end == False) and (count < auto.getSize()*100):
            count += 1
            if (current not in auto.end):
                if (word not in words):
                    words.append(word)
            trans = auto.findTransFromNode(current)
            if (not len(trans) == 0):
                delete_list = []
                for x in trans:
                    if (x.getEnd() == terminating):
                        delete_list.append(x)
                for x in delete_list:
                    trans.remove(x)
            if (not len(trans) == 0):
                random_trans = random.choice(trans)
                if (not random_trans.getEnd() == terminating):
                    current = random_trans.getEnd()
                    word += random_trans.getSymbol()
            else:
                end = True
    return words

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
print("Accepting Words: {}".format(getWords(newauto)))
