from classes import *
import random

def findAllPaths(auto): #method is to find a path add it to paths, and then add one of the transitions used in the path to a list where the next path cannot traverse, this will force a new path next iteration
    paths = []
    removedtrans = []
    check = 0
    while(check < 10):
        newpath = _findAllPaths(auto, auto.start, [], removedtrans, 0)
        if (not newpath == False):
            paths.append(newpath)
            newint = random.randint(0, len(newpath) - 2)
            for x in auto.transitions:
                if ((x.getStart() == newpath[newint]) and (x.getEnd() == newpath[newint + 1])):
                    removedtrans.append(x)
        elif(newpath == False):
            check += 1
    return paths

def _findAllPaths(auto, current, explored, removedtrans, turn): #somehow getting None type from here
    turn += 1
    if turn == auto.getSize() * 3:
        return False
    if (current in auto.end):
        return [current]
    frontier = auto.findTransFromNode(current)
    random.shuffle(frontier)
    for x in range(len(frontier)):
        next = frontier.pop()
        if (next not in removedtrans):
            newpath = _findAllPaths(auto, next.getEnd(), explored, removedtrans, turn)
            if(not newpath == False):
                return newpath.append(current)
    return False




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
