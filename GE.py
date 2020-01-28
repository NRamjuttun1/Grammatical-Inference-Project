from classes import Automaton, Node, Transition, buildAutomatonFromStrings, _buildAutomatonFromString

def test(auto):
    print(auto.checkNodeExists(auto.findNode("s10")))
    for i in range(len(auto.transitions)):
        if (auto.transitions[i].getStart().getID() == "s9"):
            print(auto.transitions[i].getSymbol())
    for i in range(len(auto.end)):
        print(auto.end[i].getID())

strs = ["cars", "drives", "good"]
auto = buildAutomatonFromStrings(strs, "s")
print(auto.checkInput("drives"))
#test(auto)
