from classes import *

def findAllPaths(auto):
    explored = []
    paths = []
    while(not len(explored) == len(auto.transitions)):
        newpath, explored = _findAllPaths(auto, auto.start, [], explored)
        if (not newpath == False):
            paths.append(newpath)
    for x in paths:
        print(str(x))

def _findAllPaths(auto, current, path, explored):
    if (current in auto.end):
        return [current]
    for x in auto.findTransFromNode(current):
        explored.append(x)
        newrun = _findAllPaths(auto, x.getEnd(), path, explored)
        if (not newrun == False):
            return path.append(current), explored
    return False, explored


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
newauto.setEnd(newauto.getNode(3))
print(newauto)
newauto.mergeNode(newauto.nodes[2], newauto.nodes[0])
print(newauto)
