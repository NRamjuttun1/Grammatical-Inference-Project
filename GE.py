from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString, mergeAutomaton, buildAutomatonFromMergeList

def test(auto):
    print(auto.checkNodeExists(auto.findNode("s10")))
    for i in range(len(auto.transitions)):
        if (auto.transitions[i].getStart().getID() == "s9"):
            print(auto.transitions[i].getSymbol())
    for i in range(len(auto.end)):
        print(auto.end[i].getID())

strs = ["cars", "drives", "good"]
auto = buildAutomatonFromStrings(strs, "G")
print(auto.checkInput("drives"))
mergeAutomaton(auto, [0,1,1,2,5,5,1,3,6,6,2,6,2,3,4])
#test(auto)
