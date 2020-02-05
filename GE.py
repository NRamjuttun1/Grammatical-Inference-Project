from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString, mergeAutomaton, buildAutomatonFromMergeList, flattenMergeList, getListPos

strs = ["cars", "drives", "good"]
auto = buildAutomatonFromStrings(strs, "G")

def test(auto):
    print(auto.checkNodeExists(auto.findNode("s10")))
    for i in range(len(auto.transitions)):
        if (auto.transitions[i].getStart().getID() == "s9"):
            print(auto.transitions[i].getSymbol())
    for i in range(len(auto.end)):
        print(auto.end[i].getID())



#print(auto.checkInput("drives"))
#print(mergeAutomaton(auto, [0,1,1,2,5,5,1,3,6,6,2,6,2,3,4]))
tempauto = mergeAutomaton(auto, [6,4,7,0,2,3,5,4,1,0,2,7,6,5,5])
print(tempauto)
print(tempauto.checkInput("good"))
#test(auto)
